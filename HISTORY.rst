=======
History
=======

* Drop Python 3.5 support.

* Support Python 3.9.

3.5.0 (2020-08-25)
------------------

* Following Django’s example in
  `Ticket #31670 <https://code.djangoproject.com/ticket/31670>`__ for replacing
  the term “whitelist”, plus an aim to make the setting names more
  comprehensible, the following settings have been renamed:

  * ``CORS_ORIGIN_WHITELIST`` -> ``CORS_ALLOWED_ORIGINS``
  * ``CORS_ORIGIN_REGEX_WHITELIST`` -> ``CORS_ALLOWED_ORIGIN_REGEXES``
  * ``CORS_ORIGIN_ALLOW_ALL`` -> ``CORS_ALLOW_ALL_ORIGINS``

  The old names will continue to work as aliases, with the new ones taking
  precedence.

3.4.0 (2020-06-19)
------------------

* Drop Django 2.0 and 2.1 support.

3.4.0 (2020-06-15)
------------------

* Add Django 3.1 support.

3.3.0 (2020-05-18)
------------------

* Drop Django 1.11 support. Only Django 2.0+ is supported now.
* Drop the ``providing_args`` argument from ``Signal`` to prevent a deprecation
  warning on Django 3.1.

3.2.1 (2020-01-04)
------------------

* Update LICENSE file to Unix line endings, fixing issues with license checker
  ``pip-licenses`` (`Issue
  #477 <https://github.com/adamchainz/django-cors-headers/issues/477>`__).

3.2.0 (2019-11-15)
------------------

* Converted setuptools metadata to configuration file. This meant removing the
  ``__version__`` attribute from the package. If you want to inspect the
  installed version, use
  ``importlib.metadata.version("django-cors-headers")``
  (`docs <https://docs.python.org/3.8/library/importlib.metadata.html#distribution-versions>`__ /
  `backport <https://pypi.org/project/importlib-metadata/>`__).
* Support Python 3.8.

3.1.1 (2019-09-30)
------------------

* Support the value `file://` for origins, which is accidentally sent by some
  versions of Chrome on Android.

3.1.0 (2019-08-13)
------------------

* Drop Python 2 support, only Python 3.5-3.7 is supported now.
* Fix all links for move from ``github.com/ottoyiu/django-cors-headers`` to
  ``github.com/adamchainz/django-cors-headers``.

3.0.2 (2019-05-28)
------------------

* Add a hint to the ``corsheaders.E013`` check to make it more obvious how to
  resolve it.

3.0.1 (2019-05-13)
------------------

* Allow 'null' in ``CORS_ORIGIN_WHITELIST`` check.

3.0.0 (2019-05-10)
------------------

* ``CORS_ORIGIN_WHITELIST`` now requires URI schemes, and optionally ports.
  This is part of the CORS specification
  (`Section 3.2 <https://tools.ietf.org/html/rfc6454#section-3.2>`_) that was
  not implemented in this library, except from with the
  ``CORS_ORIGIN_REGEX_WHITELIST`` setting. It fixes a security issue where the
  CORS middleware would allow requests between schemes, for example from
  insecure ``http://`` Origins to a secure ``https://`` site.

  You will need to update your whitelist to include schemes, for example from
  this:

  .. code-block:: python

      CORS_ORIGIN_WHITELIST = ['example.com']

  ...to this:

  .. code-block:: python

      CORS_ORIGIN_WHITELIST = ['https://example.com']

* Removed the ``CORS_MODEL`` setting, and associated class. It seems very few,
  or no users were using it, since there were no bug reports since its move to
  abstract in version 2.0.0 (2017-01-07). If you *are* using this
  functionality, you can continue by changing your model to not inherit from
  the abstract one, and add a signal handler for ``check_request_enabled`` that
  reads from your model. Note you'll need to handle the move to include schemes
  for Origins.

2.5.3 (2019-04-28)
------------------

* Tested on Django 2.2. No changes were needed for compatibility.
* Tested on Python 3.7. No changes were needed for compatibility.

2.5.2 (2019-03-15)
------------------

* Improve inclusion of tests in ``sdist`` to ignore ``.pyc`` files.

2.5.1 (2019-03-13)
------------------

* Include test infrastructure in ``sdist`` to allow consumers to use it.

2.5.0 (2019-03-05)
------------------

* Drop Django 1.8, 1.9, and 1.10 support. Only Django 1.11+ is supported now.

2.4.1 (2019-02-28)
------------------

* Fix ``DeprecationWarning`` from importing ``collections.abc.Sequence`` on
  Python 3.7.

2.4.0 (2018-07-18)
------------------

* Always add 'Origin' to the 'Vary' header for responses to enabled URL's,
  to prevent caching of responses intended for one origin being served for
  another.

2.3.0 (2018-06-27)
------------------

* Match ``CORS_URLS_REGEX`` to ``request.path_info`` instead of
  ``request.path``, so the patterns can work without knowing the site's path
  prefix at configuration time.

2.2.1 (2018-06-27)
------------------

* Add ``Content-Length`` header to CORS preflight requests. This fixes issues
  with some HTTP proxies and servers, e.g. AWS Elastic Beanstalk.

2.2.0 (2018-02-28)
------------------

* Django 2.0 compatibility. Again there were no changes to the actual library
  code, so previous versions probably work.
* Ensured that ``request._cors_enabled`` is always a ``bool()`` - previously it
  could be set to a regex match object.

2.1.0 (2017-05-28)
------------------

* Django 1.11 compatibility. There were no changes to the actual library code,
  so previous versions probably work, though they weren't properly tested on
  1.11.

2.0.2 (2017-02-06)
------------------

* Fix when the check for ``CORS_MODEL`` is done to allow it to properly add
  the headers and respond to ``OPTIONS`` requests.

2.0.1 (2017-01-29)
------------------

* Add support for specifying 'null' in ``CORS_ORIGIN_WHITELIST``.

2.0.0 (2017-01-07)
------------------

* Remove previously undocumented ``CorsModel`` as it was causing migration
  issues. For backwards compatibility, any users previously using ``CorsModel``
  should create a model in their own app that inherits from the new
  ``AbstractCorsModel``, and to keep using the same data, set the model's
  ``db_table`` to 'corsheaders_corsmodel'. Users not using ``CorsModel``
  will find they have an unused table that they can drop.
* Make sure that ``Access-Control-Allow-Credentials`` is in the response if the
  client asks for it.

1.3.1 (2016-11-09)
------------------

* Fix a bug with the single check if CORS enabled added in 1.3.0: on Django
  < 1.10 shortcut responses could be generated by middleware above
  ``CorsMiddleware``, before it processed the request, failing with an
  ``AttributeError`` for ``request._cors_enabled``. Also clarified the docs
  that ``CorsMiddleware`` should be kept as high as possible in your middleware
  stack, above any middleware that can generate such responses.

1.3.0 (2016-11-06)
------------------

* Add checks to validate the types of the settings.
* Add the 'Do Not Track' header ``'DNT'`` to the default for
  ``CORS_ALLOW_HEADERS``.
* Add 'Origin' to the 'Vary' header of outgoing requests when not allowing all
  origins, as per the CORS spec. Note this changes the way HTTP caching works
  with your CORS-enabled responses.
* Check whether CORS should be enabled on a request only once. This has had a
  minor change on the conditions where any custom signals will be called -
  signals will now always be called *before* ``HTTP_REFERER`` gets replaced,
  whereas before they could be called before and after. Also this attaches the
  attribute ``_cors_enabled`` to ``request`` - please take care that other
  code you're running does not remove it.

1.2.2 (2016-10-05)
------------------

* Add ``CorsModel.__str__`` for human-readable text
* Add a signal that allows you to add code for more intricate control over when
  CORS headers are added.

1.2.1 (2016-09-30)
------------------

* Made settings dynamically respond to changes, and which allows you to import
  the defaults for headers and methods in order to extend them.

1.2.0 (2016-09-28)
------------------

* Drop Python 2.6 support.
* Drop Django 1.3-1.7 support, as they are no longer supported.
* Confirmed Django 1.9 support (no changes outside of tests were necessary).
* Added Django 1.10 support.
* Package as a universal wheel.

1.1.0 (2014-12-15)
------------------

* django-cors-header now supports Django 1.8 with its new application loading
  system! Thanks @jpadilla for making this possible and sorry for the delay in
  making a release.

1.0.0 (2014-12-13)
------------------

django-cors-headers is all grown-up :) Since it's been used in production for
many many deployments, I think it's time we mark this as a stable release.

* Switching this middleware versioning over to semantic versioning
* #46 add user-agent and accept-encoding default headers
* #45 pep-8 this big boy up

0.13 (2014-08-14)
-----------------

* Add support for Python 3
* Updated tests
* Improved documentation
* Small bugfixes

0.12 (2013-09-24)
-----------------

* Added an option to selectively enable CORS only for specific URLs

0.11 (2013-09-24)

* Added the ability to specify a regex for whitelisting many origin hostnames
  at once

0.10 (2013-09-05)
-----------------

* Introduced port distinction for origin checking
* Use ``urlparse`` for Python 3 support
* Added testcases to project

0.06 (2013-02-18)
-----------------

* Add support for exposed response headers

0.05 (2013-01-26)
-----------------

* Fixed middleware to ensure correct response for CORS preflight requests

0.04 (2013-01-25)
-----------------

* Add ``Access-Control-Allow-Credentials`` control to simple requests

0.03 (2013-01-22)
-----------------

* Bugfix to repair mismatched default variable names

0.02 (2013-01-19)
-----------------

* Refactor/pull defaults into separate file

0.01 (2013-01-19)
-----------------

* Initial release
