
.. _Pipenv: https://pipenv.pypa.io/en/latest/

Django-Liquid
=============

A Django template backend for `Liquid <https://github.com/jg-rp/liquid>`_. Render Liquid 
templates in your Django apps.

.. image:: https://img.shields.io/pypi/v/django-liquid.svg?style=flat-square
    :target: https://pypi.org/project/django-liquid/
    :alt: Version

.. image:: https://github.com/jg-rp/django-liquid/actions/workflows/tests.yaml/badge.svg?style=flat-square
    :target: https://github.com/jg-rp/django-liquid/tree/main/tests
    :alt: Tests

.. image:: https://img.shields.io/pypi/l/django-liquid.svg?style=flat-square
    :target: https://pypi.org/project/django-liquid/
    :alt: Licence

.. image:: https://img.shields.io/pypi/pyversions/django-liquid.svg?style=flat-square
    :target: https://pypi.org/project/django-liquid/
    :alt: Python versions


Installing
----------

Install Django Liquid using `Pipenv`_:

.. code-block:: text

    $ pipenv install django-liquid

Or `pip <https://pip.pypa.io/en/stable/getting-started/>`_:

.. code-block:: text

    $ python -m pip install -U django-liquid

Links
-----

- Documentation: https://jg-rp.github.io/liquid/guides/django-liquid
- Change Log: https://github.com/jg-rp/django-liquid/blob/main/CHANGES.rst
- PyPi: https://pypi.org/project/django-liquid/
- Source Code: https://github.com/jg-rp/django-liquid
- Issue Tracker: https://github.com/jg-rp/django-liquid/issues


Contributing
------------

- Install development dependencies with `Pipenv`_

- Format code using `black <https://github.com/psf/black>`_.

- Write tests using ``unittest.TestCase``.

- Run tests with ``make test`` or ``python runtests.py``.

- Check test coverage with ``make coverage`` and open ``htmlcov/index.html`` in your
  browser.
