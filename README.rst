===================
django-cors-headers
===================

.. image:: https://img.shields.io/github/actions/workflow/status/adamchainz/django-cors-headers/main.yml?branch=main&style=for-the-badge
   :target: https://github.com/adamchainz/django-cors-headers/actions?workflow=CI

.. image:: https://img.shields.io/badge/Coverage-100%25-success?style=for-the-badge
  :target: https://github.com/adamchainz/django-cors-headers/actions?workflow=CI

.. image:: https://img.shields.io/pypi/v/django-cors-headers.svg?style=for-the-badge
    :target: https://pypi.org/project/django-cors-headers/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
    :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

A Django App that adds Cross-Origin Resource Sharing (CORS) headers to
responses. This allows in-browser requests to your Django application from
other origins.

About CORS
----------

Adding CORS headers allows your resources to be accessed on other domains. It's
important you understand the implications before adding the headers, since you
could be unintentionally opening up your site's private data to others.

Some good resources to read on the subject are:

* Julia Evans' `introductory comic <https://drawings.jvns.ca/cors/>`__ and
  `educational quiz <https://questions.wizardzines.com/cors.html>`__.
* Jake Archibald’s `How to win at CORS <https://jakearchibald.com/2021/cors/>`__
* The `MDN Article <https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS>`_
* The `HTML5 Rocks Tutorial <https://www.html5rocks.com/en/tutorials/cors/>`_
* The `Wikipedia Page <https://en.wikipedia.org/wiki/Cross-origin_resource_sharing>`_

Requirements
------------

Python 3.7 to 3.11 supported.

Django 3.2 to 4.2 supported.

----

**Want to work smarter and faster?**
Check out my book `Boost Your Django DX <https://adamchainz.gumroad.com/l/byddx>`__ which covers many ways to improve your development experience.

----

Setup
-----

Install from **pip**:

.. code-block:: sh

    python -m pip install django-cors-headers

and then add it to your installed apps:

.. code-block:: python

    INSTALLED_APPS = [
        ...,
        "corsheaders",
        ...,
    ]

Make sure you add the trailing comma or you might get a ``ModuleNotFoundError``
(see `this blog
post <https://adamj.eu/tech/2020/06/29/why-does-python-raise-modulenotfounderror-when-modifying-installed-apps/>`__).

You will also need to add a middleware class to listen in on responses:

.. code-block:: python

    MIDDLEWARE = [
        ...,
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        ...,
    ]

``CorsMiddleware`` should be placed as high as possible, especially before any
middleware that can generate responses such as Django's ``CommonMiddleware`` or
Whitenoise's ``WhiteNoiseMiddleware``. If it is not before, it will not be able
to add the CORS headers to these responses.

About
-----

**django-cors-headers** was created in January 2013 by Otto Yiu. It went
unmaintained from August 2015 and was forked in January 2016 to the package
`django-cors-middleware <https://github.com/zestedesavoir/django-cors-middleware>`_
by Laville Augustin at Zeste de Savoir.
In September 2016, Adam Johnson, Ed Morley, and others gained maintenance
responsibility for **django-cors-headers**
(`Issue 110 <https://github.com/adamchainz/django-cors-headers/issues/110>`__)
from Otto Yiu.
Basically all of the changes in the forked **django-cors-middleware** were
merged back, or re-implemented in a different way, so it should be possible to
switch back. If there's a feature that hasn't been merged, please open an issue
about it.

**django-cors-headers** has had `40+ contributors
<https://github.com/adamchainz/django-cors-headers/graphs/contributors>`__
in its time; thanks to every one of them.

Configuration
-------------

Configure the middleware's behaviour in your Django settings. You must set at
least one of three following settings:

* ``CORS_ALLOWED_ORIGINS``
* ``CORS_ALLOWED_ORIGIN_REGEXES``
* ``CORS_ALLOW_ALL_ORIGINS``

``CORS_ALLOWED_ORIGINS: Sequence[str]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A list of origins that are authorized to make cross-site HTTP requests.
The origins in this setting will be allowed, and the requesting origin will be echoed back to the client in the |access-control-allow-origin header|__.
Defaults to ``[]``.

.. |access-control-allow-origin header| replace:: ``access-control-allow-origin`` header
__ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin

An Origin is defined by `the CORS RFC Section 3.2 <https://tools.ietf.org/html/rfc6454#section-3.2>`_ as a URI scheme + hostname + port, or one of the special values ``'null'`` or ``'file://'``.
Default ports (HTTPS = 443, HTTP = 80) are optional.

The special value ``null`` is sent by the browser in `"privacy-sensitive contexts" <https://tools.ietf.org/html/rfc6454#section-6>`__, such as when the client is running from a ``file://`` domain.
The special value `file://` is sent accidentally by some versions of Chrome on Android as per `this bug <https://bugs.chromium.org/p/chromium/issues/detail?id=991107>`__.

Example:

.. code-block:: python

    CORS_ALLOWED_ORIGINS = [
        "https://example.com",
        "https://sub.example.com",
        "http://localhost:8080",
        "http://127.0.0.1:9000",
    ]

Previously this setting was called ``CORS_ORIGIN_WHITELIST``, which still works as an alias, with the new name taking precedence.

``CORS_ALLOWED_ORIGIN_REGEXES: Sequence[str | Pattern[str]]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A list of strings representing regexes that match Origins that are authorized to make cross-site HTTP requests.
Defaults to ``[]``.
Useful when ``CORS_ALLOWED_ORIGINS`` is impractical, such as when you have a large number of subdomains.

Example:

.. code-block:: python

    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^https://\w+\.example\.com$",
    ]

Previously this setting was called ``CORS_ORIGIN_REGEX_WHITELIST``, which still works as an alias, with the new name taking precedence.

``CORS_ALLOW_ALL_ORIGINS: bool``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If ``True``, all origins will be allowed.
Other settings restricting allowed origins will be ignored.
Defaults to ``False``.

Setting this to ``True`` can be *dangerous*, as it allows any website to make cross-origin requests to yours.
Generally you'll want to restrict the list of allowed origins with ``CORS_ALLOWED_ORIGINS`` or ``CORS_ALLOWED_ORIGIN_REGEXES``.

Previously this setting was called ``CORS_ORIGIN_ALLOW_ALL``, which still works as an alias, with the new name taking precedence.

--------------

The following are optional settings, for which the defaults probably suffice.

``CORS_URLS_REGEX: str | Pattern[str]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A regex which restricts the URL's for which the CORS headers will be sent.
Defaults to ``r'^.*$'``, i.e. match all URL's.
Useful when you only need CORS on a part of your site, e.g. an API at ``/api/``.

Example:

.. code-block:: python

    CORS_URLS_REGEX = r"^/api/.*$"

``CORS_ALLOW_METHODS: Sequence[str]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A list of HTTP verbs that are allowed for the actual request.
Defaults to:

.. code-block:: python

    CORS_ALLOW_METHODS = (
        "DELETE",
        "GET",
        "OPTIONS",
        "PATCH",
        "POST",
        "PUT",
    )

The default can be imported as ``corsheaders.defaults.default_methods`` so you can just extend it with your custom methods.
This allows you to keep up to date with any future changes.
For example:

.. code-block:: python

    from corsheaders.defaults import default_methods

    CORS_ALLOW_METHODS = (
        *default_methods,
        "POKE",
    )

``CORS_ALLOW_HEADERS: Sequence[str]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The list of non-standard HTTP headers that you permit in requests from the browser.
Sets the |Access-Control-Allow-Headers header|__ in responses to `preflight requests <https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request>`__.
Defaults to:

.. |Access-Control-Allow-Headers header| replace:: ``Access-Control-Allow-Headers`` header
__ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers

.. code-block:: python

    CORS_ALLOW_HEADERS = (
        "accept",
        "authorization",
        "content-type",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
    )

The default can be imported as ``corsheaders.defaults.default_headers`` so you can extend it with your custom headers.
This allows you to keep up to date with any future changes.
For example:

.. code-block:: python

    from corsheaders.defaults import default_headers

    CORS_ALLOW_HEADERS = (
        *default_headers,
        "my-custom-header",
    )

``CORS_EXPOSE_HEADERS: Sequence[str]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The list of extra HTTP headers to expose to the browser, in addition to the default `safelisted headers <https://developer.mozilla.org/en-US/docs/Glossary/CORS-safelisted_response_header>`__.
If non-empty, these are declared in the |access-control-expose-headers header|__.
Defaults to ``[]``.

.. |access-control-expose-headers header| replace:: ``access-control-expose-headers`` header
__ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Expose-Headers

``CORS_PREFLIGHT_MAX_AGE: int``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The number of seconds the browser can cache the preflight response.
This sets the |access-control-max-age header|__ in preflight responses.
If this is 0 (or any falsey value), no max age header will be sent.
Defaults to ``86400`` (one day).

.. |access-control-max-age header| replace:: ``access-control-max-age`` header
__ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Max-Age

**Note:**
Browsers send `preflight requests <https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request>`__ before certain “non-simple” requests, to check they will be allowed.
Read more about it in the `CORS MDN article <https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#preflighted_requests>`_.

``CORS_ALLOW_CREDENTIALS: bool``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If ``True``, cookies will be allowed to be included in cross-site HTTP requests.
This sets the |access-control-allow-credentials header|__ in preflight and normal responses.
Defaults to ``False``.

.. |access-control-allow-credentials header| replace:: ``Access-Control-Allow-Credentials`` header
__ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/access-control-allow-credentials

Note: in Django 2.1 the `SESSION_COOKIE_SAMESITE`_ setting was added, set to ``'Lax'`` by default, which will prevent Django's session cookie being sent cross-domain.
Change the setting to ``'None'`` if you need to bypass this security restriction.

.. _SESSION_COOKIE_SAMESITE: https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-SESSION_COOKIE_SAMESITE

``CORS_ALLOW_PRIVATE_NETWORK: bool``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If ``True``, allow requests from sites on “public” IP to this server on a “private” IP.
In such cases, browsers send an extra CORS header ``access-control-request-private-network``, for which ``OPTIONS`` responses must contain ``access-control-allow-private-network: true``.

Refer to:

* `Local Network Access <https://wicg.github.io/local-network-access/>`__, the W3C Community Draft specification.
* `Private Network Access: introducing preflights <https://developer.chrome.com/blog/private-network-access-preflight/>`__, a blog post from the Google Chrome team.

CSRF Integration
----------------

Most sites will need to take advantage of the `Cross-Site Request Forgery
protection <https://docs.djangoproject.com/en/stable/ref/csrf/>`_ that Django
offers. CORS and CSRF are separate, and Django has no way of using your CORS
configuration to exempt sites from the ``Referer`` checking that it does on
secure requests. The way to do that is with its `CSRF_TRUSTED_ORIGINS setting
<https://docs.djangoproject.com/en/stable/ref/settings/#csrf-trusted-origins>`_.
For example:

.. code-block:: python

    CORS_ALLOWED_ORIGINS = [
        "https://read-only.example.com",
        "https://read-and-write.example.com",
    ]

    CSRF_TRUSTED_ORIGINS = [
        "https://read-and-write.example.com",
    ]

Signals
-------

If you have a use case that requires more than just the above configuration,
you can attach code to check if a given request should be allowed. For example,
this can be used to read the list of origins you allow from a model. Attach any
number of handlers to the ``check_request_enabled``
`Django signal <https://docs.djangoproject.com/en/stable/ref/signals/>`_, which
provides the ``request`` argument (use ``**kwargs`` in your handler to protect
against any future arguments being added). If any handler attached to the
signal returns a truthy value, the request will be allowed.

For example you might define a handler like this:

.. code-block:: python

    # myapp/handlers.py
    from corsheaders.signals import check_request_enabled

    from myapp.models import MySite


    def cors_allow_mysites(sender, request, **kwargs):
        return MySite.objects.filter(host=request.headers["origin"]).exists()


    check_request_enabled.connect(cors_allow_mysites)

Then connect it at app ready time using a `Django AppConfig
<https://docs.djangoproject.com/en/stable/ref/applications/>`_:

.. code-block:: python

    # myapp/__init__.py

    default_app_config = "myapp.apps.MyAppConfig"

.. code-block:: python

    # myapp/apps.py

    from django.apps import AppConfig


    class MyAppConfig(AppConfig):
        name = "myapp"

        def ready(self):
            # Makes sure all signal handlers are connected
            from myapp import handlers  # noqa

A common use case for the signal is to allow *all* origins to access a subset
of URL's, whilst allowing a normal set of origins to access *all* URL's. This
isn't possible using just the normal configuration, but it can be achieved with
a signal handler.

First set ``CORS_ALLOWED_ORIGINS`` to the list of trusted origins that are
allowed to access every URL, and then add a handler to
``check_request_enabled`` to allow CORS regardless of the origin for the
unrestricted URL's. For example:

.. code-block:: python

    # myapp/handlers.py
    from corsheaders.signals import check_request_enabled


    def cors_allow_api_to_everyone(sender, request, **kwargs):
        return request.path.startswith("/api/")


    check_request_enabled.connect(cors_allow_api_to_everyone)
