Nearly drop-in replacement for selenium driver in Python::

  import saucelabs
  
  selenium = saucelabs.Selenium('127.0.0.1', '80', saucelabs.FIREFOX, USERNAME, API_KEY)

For more information, see the small amount of code in saucelabs/__init__.py, and saucelabs/tests.py