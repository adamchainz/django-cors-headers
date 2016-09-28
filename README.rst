django-cors-headers
===================

A Django App that adds CORS (Cross-Origin Resource Sharing) headers to
responses.

Although JSON-P is useful, it is strictly limited to GET requests. CORS
builds on top of ``XmlHttpRequest`` to allow developers to make cross-domain
requests, similar to same-domain requests. Read more about it here:
http://www.html5rocks.com/en/tutorials/cors/

.. image:: https://travis-ci.org/ottoyiu/django-cors-headers.png?branch=master
   :target: https://travis-ci.org/ottoyiu/django-cors-headers

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

    MIDDLEWARE_CLASSES = (
        ...
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
    )

Note that ``CorsMiddleware`` needs to come before Django's
``CommonMiddleware`` if you are using Django's ``USE_ETAGS = True``
setting, otherwise the CORS headers will be lost from 304 Not-Modified
responses, causing errors in some browsers.

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

A list of origin hostnames that are authorized to make cross-site HTTP
requests. Defaults to ``[]``.

Example:

.. code-block:: python

    CORS_ORIGIN_WHITELIST = (
        'google.com',
        'hostname.example.com'
    )

``CORS_ORIGIN_REGEX_WHITELIST``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A list of regexes that match origin regex list of origin hostnames that are
authorized to make cross-site HTTP requests. Defaults to ``[]``. Useful when
``CORS_ORIGIN_WHITELIST`` is impractical, such as when you have a large
number of subdomains.

Example:

.. code-block:: python

    CORS_ORIGIN_REGEX_WHITELIST = ('^(https?://)?(\w+\.)?google\.com$', )

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

    CORS_ALLOW_METHODS = [
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS'
    ]

``CORS_ALLOW_HEADERS``
~~~~~~~~~~~~~~~~~~~~~~

The list of non-standard HTTP headers that can be used when making the actual
request. Defaults to:

.. code-block:: python

    CORS_ALLOW_HEADERS = [
        'x-requested-with',
        'content-type',
        'accept',
        'origin',
        'authorization',
        'x-csrftoken'
    ]

``CORS_EXPOSE_HEADERS``
~~~~~~~~~~~~~~~~~~~~~~~

The list of HTTP headers that are to be exposed to the browser. Defaults to
``[]``.


``CORS_PREFLIGHT_MAX_AGE``
~~~~~~~~~~~~~~~~~~~~~~~~~~

The number of seconds a client/browser can cache the preflight response.
Defaults to ``86400``.


**Note:** A preflight request is an extra request that is made when making a
"not-so-simple" request (e.g. ``Content-Type`` is not
``application/x-www-form-urlencoded``) to determine what requests the server
actually accepts. Read more about it in the `HTML 5 Rocks CORS tutorial
<https://www.html5rocks.com/en/tutorials/cors/>`_.

``CORS_ALLOW_CREDENTIALS``
~~~~~~~~~~~~~~~~~~~~~~~~~~

If ``True``, cookies will be allowed to be included in cross-site HTTP
requests. Defaults to ``False``.

``CORS_REPLACE_HTTPS_REFERER``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If ``True``, the ``HTTP_REFERER`` header will get replaced when CORS checks
pass, so that the Django CSRF middleware checks work with HTTPS. Defaults to
``False``.

**Note:** With this feature enabled, you also need to add
``corsheaders.middleware.CorsPostCsrfMiddleware`` after
``django.middleware.csrf.CsrfViewMiddleware`` in your ``MIDDLEWARE_CLASSES`` to
undo the header replacement.


Changelog
---------

v0.13 and onwards - `Release
Notes <https://github.com/ottoyiu/django-cors-headers/releases>`__

v0.12 - Added an option to selectively enable CORS only for specific
URLs

v0.11 - Added the ability to specify a regex for whitelisting many
origin hostnames at once

v0.10 - Introduced port distinction for origin checking; use
``urlparse`` for Python 3 support; added testcases to project

v0.06 - Add support for exposed response headers

v0.05 - fixed middleware to ensure correct response for CORS preflight
requests

v0.04 - add Access-Control-Allow-Credentials control to simple requests

v0.03 - bugfix (repair mismatched default variable names)

v0.02 - refactor/pull defaults into separate file

v0.01 - initial release

Credits
-------

A shoutout to everyone who has contributed:

-  Otto Yiu - `@ottoyiu <https://github.com/ottoyiu>`_
-  Michael Tom-Wing - `@mtomwing <https://github.com/mtomwing>`_
-  Darrin Massena - `@darrinm <https://github.com/darrinm>`_
-  Paul Dufour - `@pdufour <https://github.com/pdufour>`_
-  Lukasz Balcerzak - `@lukaszb <https://github.com/lukaszb>`_
-  Keita Oouchi - `@keitaoouchi <https://github.com/keitaoouchi>`_
-  Orlando Pozo - `@opozo <https://github.com/opozo>`_
-  Toran Billups - `@toranb <https://github.com/toranb>`_
-  Raymond Penners - `@pennersr <https://github.com/pennersr>`_
-  Markus Kaiserswerth - `@mkai <https://github.com/mkai>`_
-  ...and `many others!
   <https://github.com/ottoyiu/django-cors-headers/graphs/contributors>`_
