Django-Liquid
=============

A Django template backend for `Liquid <https://github.com/jg-rp/liquid>`_. Render Liquid 
templates in your Django apps.

.. image:: https://img.shields.io/pypi/v/django-liquid.svg
    :target: https://pypi.org/project/django-liquid/
    :alt: Version

.. image:: https://img.shields.io/pypi/l/django-liquid.svg
    :target: https://pypi.org/project/django-liquid/
    :alt: Licence

.. image:: https://img.shields.io/pypi/pyversions/django-liquid.svg
    :target: https://pypi.org/project/django-liquid/
    :alt: Python versions


Installing
----------

Install and update using `pip <https://pip.pypa.io/en/stable/quickstart/>`_:

.. code-block:: text

    $ python -m pip install -U django-liquid


Quick Start
-----------

.. _Django for Jinja2: https://docs.djangoproject.com/en/3.2/topics/templates/#django.template.backends.jinja2.Jinja2

If you're already familiar with configuring `Django for Jinja2`_, Liquid works in almost
exactly the same way. Just with less options. Simply set ``BACKEND`` to 
``django_liquid.liquid.Liquid``.

Add configuration for the Liquid template engine to your Django project's
``settings.py`` file. Starting with the default ``TEMPLATE`` configuration after running 
``django-admin startproject mysite``, basic Liquid configuration would look like this.

.. code-block:: python

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
        {
            'BACKEND': 'django_liquid.liquid.Liquid',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {},
        },
    ]

When ``APP_DIRS`` is ``True``, Liquid engines look for templates in the ``liquid``
subdirectory of installed applications.

``OPTIONS`` are passed to the ``liquid.Environment`` constructor. The default 
``Environment`` is configured as follows.

- ``autoescape``: ``True``
- ``loader``: a ``FileSystemLoader`` configured for ``DIRS`` and ``APP_DIRS``
- ``undefined``: ``DebugUndefined`` if ``settings.DEBUG`` else ``Undefined``

Render Liquid templates from your app views just like any other Django template backend.

.. code-block:: python

    from django.shortcuts import render

    def index(request):
        context = {"greeting": "hello"}
        return render(request, 'myapp/index.liquid', context)

If you've got multiple template engines configured, like in the example above, Django
will use the first engine and template it finds matching the given template name. You
can force Django to use a specific template engine with the ``using`` argument.

.. code-block:: python

    from django.shortcuts import render

    def index(request):
        context = {"greeting": "hello"}
        return render(request, 'myapp/index.html', context, using='liquid')

Environment Factory
-------------------

.. _python-liquid-extra: https://github.com/jg-rp/liquid-extra

You can configure your ``liquid.Environment`` with additional tags or filters by setting
the ``environment`` template backend option to the name of an ``Environment`` factory
function. Lets say you want to register the ``json`` filter from `python-liquid-extra`_.
If the following is saved as ``myproject/liquid.py``

.. code-block:: python

    from liquid import Environment
    from liquid_extra import filters
    
    def environment(**options):
        env = Environment(**options)
        env.add_filter("json", filters.JSON())
        # Register more filters or tags here.
        return env

Then tell the django template backend to use your environment factory function like
this.

.. code-block:: python

    # settings.py
    TEMPLATES = [
        {
            'BACKEND': 'django_liquid.liquid.Liquid',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
              'environment': 'myproject.liquid.environment'
            },
        },
    ]

Contributing
------------

.. _Pylance: https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance
.. _Pyright: https://github.com/microsoft/pyright

- Install development dependencies with `Pipenv <https://github.com/pypa/pipenv>`_
- Python Liquid fully embraces type hints and static type checking. I like to use the
  `Pylance`_ extension for Visual Studio Code, which includes `Pyright`_ for static type
  checking.
- Format code using `black <https://github.com/psf/black>`_.
- Write tests using ``unittest.TestCase``.
- Run tests with ``make test``.
- Check test coverage with ``make coverage`` and open ``htmlcov/index.html`` in your
  browser.
        