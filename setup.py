#!/usr/bin/env python

# Credit to bartTC and https://github.com/bartTC/django-memcache-status for ideas

try:
    from setuptools import setup, find_packages
    from setuptools.command.test import test
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    from setuptools.command.test import test


class mytest(test):
    def run(self, *args, **kwargs):
        from runtests import runtests
        runtests()

setup(
    name='selenium-saucelabs-python',
    version='0.3.1',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='http://github.com/dcramer/selenium-saucelabs-python',
    description = 'Sauce OnDemand driver for Python',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'simplejson',
    ],
    test_suite = 'saucelabs.tests',
    include_package_data=True,
    cmdclass={"test": mytest},
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)