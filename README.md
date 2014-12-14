django-cors-headers
==================

A Django App that adds CORS (Cross-Origin Resource Sharing) headers to responses.

Although JSON-P is useful, it is strictly limited to GET requests. CORS builds on top of XmlHttpRequest to allow developers to make cross-domain requests, similar to same-domain requests. Read more about it here: [http://www.html5rocks.com/en/tutorials/cors/ ](http://www.html5rocks.com/en/tutorials/cors/)

[![Build Status](https://travis-ci.org/ottoyiu/django-cors-headers.png?branch=master)](https://travis-ci.org/ottoyiu/django-cors-headers)

## Setup ##
Install by downloading the source and running:

>   python setup.py install

or

>   pip install django-cors-headers

and then add it to your installed apps:

    INSTALLED_APPS = (
        ...
        'corsheaders',
        ...
    )

You will also need to add a middleware class to listen in on responses:

    MIDDLEWARE_CLASSES = (
        ...
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
    )

Note that `CorsMiddleware` needs to come before Django's `CommonMiddleware` if you are using Django's `USE_ETAGS = True` setting, otherwise the CORS headers will be lost from the 304 not-modified responses, causing errors in some browsers.

## Configuration ##

Add hosts that are allowed to do cross-site requests to `CORS_ORIGIN_WHITELIST` or set `CORS_ORIGIN_ALLOW_ALL` to `True` to allow all hosts.


>CORS\_ORIGIN\_ALLOW\_ALL: if True, the whitelist will not be used and all origins will be accepted

    Default:

        CORS_ORIGIN_ALLOW_ALL = False

>CORS\_ORIGIN\_WHITELIST: specify a list of origin hostnames that are authorized to make a cross-site HTTP request

    Example:

        CORS_ORIGIN_WHITELIST = (
            'google.com',
            'hostname.example.com'
        )


    Default:

        CORS_ORIGIN_WHITELIST = ()

>CORS\_ORIGIN\_REGEX\_WHITELIST: specify a regex list of origin hostnames that are authorized to make a cross-site HTTP request; Useful when you have a large amount of subdomains for instance.

    Example:

        CORS_ORIGIN_REGEX_WHITELIST = ('^(https?://)?(\w+\.)?google\.com$', )


    Default:

        CORS_ORIGIN_REGEX_WHITELIST = ()


---


You may optionally specify these options in settings.py to override the defaults. Defaults are shown below:


>CORS\_URLS\_REGEX: specify a URL regex for which to enable the sending of CORS headers; Useful when you only want to enable CORS for specific URLs, e. g. for a REST API under ``/api/``.

    Example:

        CORS_URLS_REGEX = r'^/api/.*$'

    Default:

        CORS_URLS_REGEX = '^.*$'

>CORS\_ALLOW\_METHODS: specify the allowed HTTP methods that can be used when making the actual request

    Default:

        CORS_ALLOW_METHODS = (
            'GET',
            'POST',
            'PUT',
            'PATCH',
            'DELETE',
            'OPTIONS'
        )

>CORS\_ALLOW\_HEADERS: specify which non-standard HTTP headers can be used when making the actual request

    Default:

        CORS_ALLOW_HEADERS = (
            'x-requested-with',
            'content-type',
            'accept',
            'origin',
            'authorization',
            'x-csrftoken'
        )

>CORS\_EXPOSE\_HEADERS: specify which HTTP headers are to be exposed to the browser

    Default:

        CORS_EXPOSE_HEADERS = ()

>CORS\_PREFLIGHT\_MAX\_AGE: specify the number of seconds a client/browser can cache the preflight response

    Note: A preflight request is an extra request that is made when making a "not-so-simple" request (eg. content-type is not application/x-www-form-urlencoded) to determine what requests the server actually accepts. Read more about it here: [http://www.html5rocks.com/en/tutorials/cors/](http://www.html5rocks.com/en/tutorials/cors/)

    Default:

        CORS_PREFLIGHT_MAX_AGE = 86400

>CORS\_ALLOW\_CREDENTIALS: specify whether or not cookies are allowed to be included in cross-site HTTP requests (CORS).

    Default:

        CORS_ALLOW_CREDENTIALS = False

>CORS\_REPLACE\_HTTPS\_REFERER: specify whether to replace the HTTP_REFERER header if CORS checks pass so that CSRF django middleware checks will work with https

    Note: With this feature enabled, you also need to add the corsheaders.middleware.CorsPostCsrfMiddleware after django.middleware.csrf.CsrfViewMiddleware to undo the header replacement

    Default:

        CORS_REPLACE_HTTPS_REFERER = False

## Changelog ##
v0.13 and onwards - [Release Notes](https://github.com/ottoyiu/django-cors-headers/releases)

v0.12 - Added an option to selectively enable CORS only for specific URLs

v0.11 - Added the ability to specify a regex for whitelisting many origin hostnames at once

v0.10 - Introduced port distinction for origin checking; use ``urlparse`` for Python 3 support; added testcases to project

v0.06 - Add support for exposed response headers

v0.05 - fixed middleware to ensure correct response for CORS preflight requests

v0.04 - add Access-Control-Allow-Credentials control to simple requests

v0.03 - bugfix (repair mismatched default variable names)

v0.02 - refactor/pull defaults into separate file

v0.01 - initial release

## Credits ##
A shoutout to everyone who has contributed:

- Otto Yiu - [@ottoyiu](https://github.com/ottoyiu)
- Michael Tom-Wing - [@mtomwing](https://github.com/mtomwing)
- Darrin Massena - [@darrinm](https://github.com/darrinm)
- Paul Dufour - [@pdufour](https://github.com/pdufour)
- Lukasz Balcerzak - [@lukaszb](https://github.com/lukaszb)
- Keita Oouchi - [@keitaoouchi](https://github.com/keitaoouchi)
- Orlando Pozo - [@opozo](https://github.com/opozo)
- Toran Billups - [@toranb](https://github.com/toranb)
- Raymond Penners - [@pennersr](https://github.com/pennersr)
- Markus Kaiserswerth - [@mkai](https://github.com/mkai)
- and many others! - [Contributors](https://github.com/ottoyiu/django-cors-headers/graphs/contributors)
