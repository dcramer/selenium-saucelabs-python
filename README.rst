Nearly drop-in replacement for selenium driver in Python::

  import saucelabs
  
  selenium = saucelabs.Selenium('127.0.0.1', '80', saucelabs.FIREFOX, USERNAME, API_KEY)