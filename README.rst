Nearly drop-in replacement for selenium driver in Python which allows easy integration with Sauce OnDemand.

For more information about Sauce OnDemand, please visit their website: https://saucelabs.com/

Install
-------

Installation is easy using pip or setuptools::

  pip install selenium-saucelabs-python
  
Usage
-----

Integration is almost identical to the selenium driver::

  import saucelabs

  selenium = saucelabs.Selenium(host='127.0.0.1', port='80', browser=saucelabs.FIREFOX, 
                                sauceUsername=USERNAME, sauceApiKey=API_KEY)

The following variables may be passed to the constructor:

- ``host``
- ``port``
- ``browser``
- ``sauceUsername``
- ``sauceApiKey``
- ``sauceDomain``
- ``sauceConnect``: defaults to ``'sauce_connect'``; path to sauce connect binary
- ``os``: defaults to ``LINUX``
- ``browserVersion``: defaults to ``''``
- ``build``: defaults to ``None``
- ``customData``: defaults to ``{}``

The ``setJobInfo`` api is also available within the driver::

  selenium.setJobInfo(name='foo', tags=['a', 'b', 'c'], passed=True)

For more information, see the small amount of code in saucelabs/__init__.py, and saucelabs/tests.py