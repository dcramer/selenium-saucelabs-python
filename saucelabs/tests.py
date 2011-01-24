import saucelabs
import os
import unittest

assert os.environ.get('SAUCE_USERNAME') and os.environ.get('SAUCE_API_KEY'), \
       'Missing SAUCE_USERNAME or SAUCE_API_KEY environment variables'

class TestGoogle(unittest.TestCase):
    def setUp(self):
        self.selenium = saucelabs.Selenium(
            host="localhost",
            port=80,
            browser=saucelabs.FIREFOX,
            browserURL='http://www.google.com/webhp',
            sauceDomain='dummydomain.com',
            sauceUsername=os.environ['SAUCE_USERNAME'],
            sauceApiKey=os.environ['SAUCE_API_KEY'],
        )
        self.selenium.start()
        
    def test_google(self):
        sel = self.selenium
        sel.open("http://www.google.com/webhp")
        sel.type("q", "hello world")
        sel.click("btnG")
        # Google uses ajax now, so we dont need to wait
        # sel.wait_for_page_to_load(5000)
        self.assertEqual("hello world - Google Search", sel.get_title())
    
    def tearDown(self):
        self.selenium.stop()

if __name__ == "__main__":
    unittest.main()
