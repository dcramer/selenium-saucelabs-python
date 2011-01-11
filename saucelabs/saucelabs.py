from __future__ import absolute_import

# Try global selenium library first
try:
    from selenium import selenium as SeleniumBase
except ImportError:
    from saucelabs.selenium import selenium as SeleniumBase

import subprocess
import urlparse

class Selenium(SeleniumBase):
    """
    Drop-in replacement for selenium driver. Connects directly to sauce labs
    and requires no browser or selenium rc install.
    
    You will need Sauce Connect available on PATH, or specified via ``sauceConnect``
    on init.
    
    For more information, see http://saucelabs.com/docs/sauce-connect
    """
    
    def __init__(self, host, port, browserStartCommand, browserURL, sauceUsername,
                 sauceApiKey, sauceConnect=None, ):
        super(Selenium, self).__init__(host, port, browserStartCommand, browserURL)
        self.sauceConnect = sauceConnect
    
    def start_sauce_tunnel(self):
        "Starts the SauceLabs tunnel with sauce-connect."
        domain = urlparse.urlparse(self.browserURL).domain
        
        p = subprocess.Popen([self.sauceConnect, '-u', self.sauceUsername, '-k', self.sauceApiKey,
                              '-s', self.host, '-p', self.port, '-d', domain], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.STDOUT)

    def start(self, *args, **kwargs):
        "Initiates a sauce tunnel followed by a selenium instance"
        self.start_sauce_tunnel()
        return super(Selenium, self).start(*args, **kwargs)
selenium = Selenium