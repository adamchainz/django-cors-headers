History
=======

Pending
-------

* New release notes go here.

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
* Improved docuemntation
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
