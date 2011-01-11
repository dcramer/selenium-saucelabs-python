from __future__ import absolute_import

# Try global selenium library first
try:
    from selenium import selenium as SeleniumBase
except ImportError:
    from saucelabs.selenium import selenium as SeleniumBase

import simplejson
import subprocess
import urlparse

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
    
    def __init__(self, host, port, browser, browserURL, sauceUsername,
                 sauceApiKey, sauceConnect=None, os=LINUX, browserVersion=''):
        """
        Additional parameters for Sauce OnDemand:

        - sauceConnect: binary path to sauce_connect script
        - os: operating system name
        - browserVersion: browser version number
        """
        self.sauceConnect = sauceConnect

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
        }
        if os:
            browserArgs['os'] = os
        if browserVersion:
            browserArgs['browser-version'] = browserVersion
    
        super(Selenium, self).__init__(host, port, simplejson.dumps(browserArgs), browserURL)
    
    def start_sauce_tunnel(self):
        "Starts the Sauce OnDemand tunnel with sauce-connect."

        domain = urlparse.urlparse(self.browserURL).domain
        
        self.sauceTunnel = subprocess.Popen([self.sauceConnect, '-u', self.sauceUsername, '-k', self.sauceApiKey,
                              '-s', self.host, '-p', self.port, '-d', domain], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.STDOUT)
    
    def stop_sauce_tunnel(self):
        self.sauceTunnel.terminate()

    def start(self, *args, **kwargs):
        "Initiates a sauce tunnel followed by a selenium instance."

        self.start_sauce_tunnel()

        return super(Selenium, self).start(*args, **kwargs)

    def stop(self, *args, **kwargs):
        "Completes Sauce OnDemand tunnel connection."

        result = super(Selenium, self).start(*args, **kwargs)

        self.stop_sauce_tunnel()

        return result
    
    def setJobInfo(self, **kwargs):
        self.set_context("sauce:job-info=%s" % simplejson.dumps(kwargs));

# Maintain namespace
selenium = Selenium