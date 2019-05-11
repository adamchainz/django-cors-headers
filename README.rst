django-cors-headers
===================

.. image:: https://travis-ci.org/ottoyiu/django-cors-headers.svg?branch=master
   :target: https://travis-ci.org/ottoyiu/django-cors-headers

.. image:: https://img.shields.io/pypi/v/django-cors-headers.svg
    :target: https://pypi.python.org/pypi/django-cors-headers/

A Django App that adds Cross-Origin Resource Sharing (CORS) headers to
responses. This allows in-browser requests to your Django application from
other origins.

About CORS
----------

Adding CORS headers allows your resources to be accessed on other domains. It's
important you understand the implications before adding the headers, since you
could be unintentionally open up your site's private data to others.

Some good resources to read on the subject are:

* The `Wikipedia Page <https://en.m.wikipedia.org/wiki/Cross-origin_resource_sharing>`_
* The `MDN Article <https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS>`_
* The `HTML5 Rocks Tutorial <https://www.html5rocks.com/en/tutorials/cors/>`_

Requirements
------------

Tested with all combinations of:

* Python: 2.7, 3.5, 3.6, 3.7
* Django: 1.11, 2.0, 2.1, 2.2

Setup
-----

Install from **pip**:

.. code-block:: sh

    pip install django-cors-headers

and then add it to your installed apps:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'corsheaders',
        ...
    )

You will also need to add a middleware class to listen in on responses:

.. code-block:: python

    MIDDLEWARE = [  # Or MIDDLEWARE_CLASSES on Django < 1.10
        ...
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
    ]

``CorsMiddleware`` should be placed as high as possible, especially before any
middleware that can generate responses such as Django's ``CommonMiddleware`` or
Whitenoise's ``WhiteNoiseMiddleware``. If it is not before, it will not be able
to add the CORS headers to these responses.

Also if you are using ``CORS_REPLACE_HTTPS_REFERER`` it should be placed before
Django's ``CsrfViewMiddleware`` (see more below).

About
-----

**django-cors-headers** was created in January 2013 by Otto Yiu. It went
unmaintained from August 2015 and was forked in January 2016 to the package
`django-cors-middleware <https://github.com/zestedesavoir/django-cors-middleware>`_
by Laville Augustin at Zeste de Savoir.
In September 2016, Adam Johnson, Ed Morley, and others gained maintenance
responsibility for **django-cors-headers**
(`Issue 110 <https://github.com/ottoyiu/django-cors-headers/issues/110>`_) from
Otto Yiu.
Basically all of the changes in the forked **django-cors-middleware** were
merged back, or re-implemented in a different way, so it should be possible to
switch back. If there's a feature that hasn't been merged, please open an issue
about it.

**django-cors-headers** has had `40+
contributors <https://github.com/ottoyiu/django-cors-headers/graphs/contributors>`_
in its time; thanks to every one of them.

Configuration
-------------

Configure the middleware's behaviour in your Django settings. You must add the
hosts that are allowed to do cross-site requests to
``CORS_ORIGIN_WHITELIST``, or set ``CORS_ORIGIN_ALLOW_ALL`` to ``True``
to allow all hosts.

``CORS_ORIGIN_ALLOW_ALL``
~~~~~~~~~~~~~~~~~~~~~~~~~
If ``True``, the whitelist will not be used and all origins will be accepted.
Defaults to ``False``.

``CORS_ORIGIN_WHITELIST``
~~~~~~~~~~~~~~~~~~~~~~~~~

A list of origins that are authorized to make cross-site HTTP requests.
Defaults to ``[]``.

An Origin is defined by
`the CORS RFC Section 3.2 <https://tools.ietf.org/html/rfc6454#section-3.2>`_
as a URI scheme + hostname + port, or the special value `'null'`.
Default ports (HTTPS = 443, HTTP = 80) are optional here.
The special value `null` is sent by the browser in
`"privacy-sensitive contexts" <https://tools.ietf.org/html/rfc6454#section-6>`_,
such as when the client is running from a ``file://`` domain.

Example:

.. code-block:: python

    CORS_ORIGIN_WHITELIST = [
        "https://example.com",
        "https://sub.example.com",
        "http://localhost:8080",
        "http://127.0.0.1:9000"
    )


``CORS_ORIGIN_REGEX_WHITELIST``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A list of strings representing regexes that match Origins that are authorized
to make cross-site HTTP requests. Defaults to ``[]``. Useful when
``CORS_ORIGIN_WHITELIST`` is impractical, such as when you have a large number
of subdomains.

Example:

.. code-block:: python

    CORS_ORIGIN_REGEX_WHITELIST = [
        r"^https://\w+\.example\.com$",
    ]

--------------

The following are optional settings, for which the defaults probably suffice.

``CORS_URLS_REGEX``
~~~~~~~~~~~~~~~~~~~

A regex which restricts the URL's for which the CORS headers will be sent.
Defaults to ``r'^.*$'``, i.e. match all URL's. Useful when you only need CORS
on a part of your site, e.g. an API at ``/api/``.

Example:

.. code-block:: python

    CORS_URLS_REGEX = r'^/api/.*$'

``CORS_ALLOW_METHODS``
~~~~~~~~~~~~~~~~~~~~~~

A list of HTTP verbs that are allowed for the actual request. Defaults to:

.. code-block:: python

    CORS_ALLOW_METHODS = (
        'DELETE',
        'GET',
        'OPTIONS',
        'PATCH',
        'POST',
        'PUT',
    )

The default can be imported as ``corsheaders.defaults.default_methods`` so you
can just extend it with your custom methods. This allows you to keep up to date
with any future changes. For example:

.. code-block:: python

    from corsheaders.defaults import default_methods

    CORS_ALLOW_METHODS = default_methods + (
        'POKE',
    )

``CORS_ALLOW_HEADERS``
~~~~~~~~~~~~~~~~~~~~~~

The list of non-standard HTTP headers that can be used when making the actual
request. Defaults to:

.. code-block:: python

    CORS_ALLOW_HEADERS = (
        'accept',
        'accept-encoding',
        'authorization',
        'content-type',
        'dnt',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with',
    )

The default can be imported as ``corsheaders.defaults.default_headers`` so you
can extend it with your custom headers. This allows you to keep up to date with
any future changes. For example:

.. code-block:: python

    from corsheaders.defaults import default_headers

    CORS_ALLOW_HEADERS = default_headers + (
        'my-custom-header',
    )

``CORS_EXPOSE_HEADERS``
~~~~~~~~~~~~~~~~~~~~~~~

The list of HTTP headers that are to be exposed to the browser. Defaults to
``[]``.


``CORS_PREFLIGHT_MAX_AGE``
~~~~~~~~~~~~~~~~~~~~~~~~~~

The number of seconds a client/browser can cache the preflight response. If
this is 0 (or any falsey value), no max age header will be sent. Defaults to
``86400`` (one day).


**Note:** A preflight request is an extra request that is made when making a
"not-so-simple" request (e.g. ``Content-Type`` is not
``application/x-www-form-urlencoded``) to determine what requests the server
actually accepts. Read more about it in the
`CORS MDN article <https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#Preflighted_requests>`_.

``CORS_ALLOW_CREDENTIALS``
~~~~~~~~~~~~~~~~~~~~~~~~~~

If ``True``, cookies will be allowed to be included in cross-site HTTP
requests. Defaults to ``False``.

Note: in Django 2.1 the `SESSION_COOKIE_SAMESITE`_ setting was added, set to
``'Lax'`` by default, which will prevent Django's session cookie being sent
cross-domain. Change it to ``None`` to bypass this security restriction.

.. _SESSION_COOKIE_SAMESITE: https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SESSION_COOKIE_SAMESITE

CSRF Integration
----------------

Most sites will need to take advantage of the `Cross-Site Request Forgery
protection <https://docs.djangoproject.com/en/dev/ref/csrf/>`_ that Django
offers. CORS and CSRF are separate, and Django has no way of using your CORS
configuration to exempt sites from the ``Referer`` checking that it does on
secure requests. The way to do that is with its `CSRF_TRUSTED_ORIGINS setting
<https://docs.djangoproject.com/en/dev/ref/settings/#csrf-trusted-origins>`_.
For example:

.. code-block:: python

    CORS_ORIGIN_WHITELIST = (
        'http://read.only.com',
        'http://change.allowed.com',
    )

    CSRF_TRUSTED_ORIGINS = (
        'change.allowed.com',
    )

``CORS_REPLACE_HTTPS_REFERER``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``CSRF_TRUSTED_ORIGINS`` was introduced in Django 1.9, so users of earlier
versions will need an alternate solution. If ``CORS_REPLACE_HTTPS_REFERER`` is
``True``, ``CorsMiddleware`` will change the ``Referer`` header to something
that will pass Django's CSRF checks whenever the CORS checks pass. Defaults to
``False``.

Note that unlike ``CSRF_TRUSTED_ORIGINS``, this setting does not allow you to
distinguish between domains that are trusted to *read* resources by CORS and
domains that are trusted to *change* resources by avoiding CSRF protection.

With this feature enabled you should also add
``corsheaders.middleware.CorsPostCsrfMiddleware`` after
``django.middleware.csrf.CsrfViewMiddleware`` in your ``MIDDLEWARE_CLASSES`` to
undo the ``Referer`` replacement:

.. code-block:: python

    MIDDLEWARE_CLASSES = [
        ...
        'corsheaders.middleware.CorsMiddleware',
        ...
        'django.middleware.csrf.CsrfViewMiddleware',
        'corsheaders.middleware.CorsPostCsrfMiddleware',
        ...
    ]

Signals
-------

If you have a use case that requires more than just the above configuration,
you can attach code to check if a given request should be allowed. For example,
this can be used to read the list of origins you allow from a model. Attach any
number of handlers to the ``check_request_enabled``
`Django signal <https://docs.djangoproject.com/en/1.10/ref/signals/>`_, which
provides the ``request`` argument (use ``**kwargs`` in your handler to protect
against any future arguments being added). If any handler attached to the
signal returns a truthy value, the request will be allowed.

For example you might define a handler like this:

.. code-block:: python

    # myapp/handlers.py
    from corsheaders.signals import check_request_enabled

    from myapp.models import MySite

    def cors_allow_mysites(sender, request, **kwargs):
        return MySite.objects.filter(host=request.host).exists()

    check_request_enabled.connect(cors_allow_mysites)

Then connect it at app ready time using a `Django AppConfig
<https://docs.djangoproject.com/en/1.10/ref/applications/>`_:

.. code-block:: python

    # myapp/__init__.py

    default_app_config = 'myapp.apps.MyAppConfig'

.. code-block:: python

    # myapp/apps.py

    from django.apps import AppConfig

    class MyAppConfig(AppConfig):
        name = 'myapp'

        def ready(self):
            # Makes sure all signal handlers are connected
            from myapp import handlers  # noqa

A common use case for the signal is to allow *all* origins to access a subset
of URL's, whilst allowing a normal set of origins to access *all* URL's. This
isn't possible using just the normal configuration, but it can be achieved with
a signal handler.

First set ``CORS_ORIGIN_WHITELIST`` to the list of trusted origins that are
allowed to access every URL, and then add a handler to
``check_request_enabled`` to allow CORS regardless of the origin for the
unrestricted URL's. For example:

.. code-block:: python

    # myapp/handlers.py
    from corsheaders.signals import check_request_enabled

    def cors_allow_api_to_everyone(sender, request, **kwargs):
        return request.path.startswith('/api/')

    check_request_enabled.connect(cors_allow_api_to_everyone)
