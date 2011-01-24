"""
selenium-saucelabs-python
~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from __future__ import absolute_import

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('selenium-saucelabs-python').version
except Exception, e:
    VERSION = 'unknown'

# Try global selenium library first
try:
    from selenium import selenium as SeleniumBase
except ImportError:
    from saucelabs.selenium import selenium as SeleniumBase

import simplejson
import subprocess
import sys
import time

SAUCE_CONNECT_TIMEOUT = 60

FIREFOX = 'firefox'
IE = 'ie'
SAFARI = 'safari'
CHROME = 'googlechrome'

LINUX = 'Linux'
WINDOWS = 'Windows'

class Selenium(SeleniumBase):
    """
    Drop-in replacement for selenium driver. Connects directly to sauce labs
    and requires no browser or selenium rc install.
    
    You will need Sauce Connect available on PATH, or specified via ``sauceConnect``
    on init.
    
    For more information, see http://saucelabs.com/docs/sauce-connect
    """
    
    def __init__(self, host, port, browser, sauceUsername, sauceApiKey, sauceDomain,
                 browserURL='http://saucelabs.com', sauceConnect='sauce_connect', os=LINUX, browserVersion='',
                 build=None, customData={}):
        """
        Additional parameters for Sauce OnDemand:

        - sauceConnect: binary path to sauce_connect script
        - os: operating system name
        - browserVersion: browser version number
        """
        assert sauceUsername, 'sauceUsername cannot be empty'
        assert sauceApiKey, 'sauceApiKey cannot be empty'

        self.sauceUsername = sauceUsername
        self.sauceApiKey = sauceApiKey
        self.sauceConnect = sauceConnect
        self.sauceDomain = sauceDomain

        self.serverHost = host
        self.serverPort = port

        # Swap out host/port with Sauce OnDemand
        host = 'ondemand.saucelabs.com'
        port = '80'

        # Browser start command needs to be JSON packet
        browserArgs = {
            'username': sauceUsername,
            'access-key': sauceApiKey,
            'browser': browser,
            'build': build,
            'custom-data': customData,
        }
        if os:
            browserArgs['os'] = os
        if browserVersion:
            browserArgs['browser-version'] = browserVersion
    
        SeleniumBase.__init__(self, host, port, simplejson.dumps(browserArgs), browserURL)
    
    def start_sauce_tunnel(self):
        "Starts the Sauce OnDemand tunnel with sauce-connect."

        cmd = [self.sauceConnect, '-u', self.sauceUsername, '-k', self.sauceApiKey,
               '-s', self.serverHost, '-p', self.serverPort, '-t', self.serverPort]
        if isinstance(self.sauceDomain, (list, tuple)):
            for domain in self.sauceDomain:
                cmd.extend(['-d', domain])
        else:
            cmd.extend(['-d', self.sauceDomain])
        
        self.sauceTunnel = subprocess.Popen(map(str, cmd), stdout=subprocess.PIPE)
        start = time.time()
        while True:
            line = self.sauceTunnel.stdout.readline()
            sys.stdout.write(line)
            if line.strip().endswith('You may start your tests.'):
                break
            if time.time() - start > SAUCE_CONNECT_TIMEOUT:
                self.stop_sauce_tunnel()
                raise Exception('sauce_connect failed to come online in %s seconds' % SAUCE_CONNECT_TIMEOUT)
    
    def stop_sauce_tunnel(self):
        self.sauceTunnel.terminate()
        self.sauceTunnel.wait()

    def start_selenium(self, *args, **kwargs):
        result = self.get_string("getNewBrowserSession", [self.browserStartCommand, self.browserURL, self.extensionJs])

        self.sessionId = result
        print >> sys.stdout, "SauceOnDemandSessionID=" + result
        
        return result

    def stop_selenium(self, *args, **kwargs):
        return SeleniumBase.stop(self, *args, **kwargs)

    def start(self, *args, **kwargs):
        "Initiates a sauce tunnel followed by a selenium instance."

        self.start_sauce_tunnel()

        return self.start_selenium(*args, **kwargs)

    def stop(self, *args, **kwargs):
        "Completes Sauce OnDemand tunnel connection."

        result = self.stop_selenium(*args, **kwargs)

        self.stop_sauce_tunnel()

        return result
    
    def setJobInfo(self, **kwargs):
        self.set_context("sauce:job-info=%s" % simplejson.dumps(kwargs));

# Maintain namespace
selenium = Selenium