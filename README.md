django-cors-headers
==================

A Django App that adds CORS (Cross-Origin Resource Sharing) headers to responses. 

Although JSON-P is useful, it is strictly limited to GET requests. CORS builds on top of XmlHttpRequest to allow developers to make cross-domain requests, similar to same-domain requests. Read more about it here: [http://www.html5rocks.com/en/tutorials/cors/ ](http://www.html5rocks.com/en/tutorials/cors/)


## Setup ##
Install by downloading the source and running:

>	python setup.py install

or

>	pip install django-cors-headers

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
        ...
    )

## Configuration ##

You may optionally specify these options in settings.py to override the defaults. Defaults are shown below:


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
    		'authorization'
		)

>CORS\_ORIGIN\_ALLOW\_ALL: if True, the whitelist will not be used and all origins will be accepted

    Default:

        CORS_ORIGIN_ALLOW_ALL = False

>CORS\_ORIGIN\_WHITELIST: specify a list of origin hostnames that are authorized to make a cross-site HTTP request; set to None to allow access to anyone

	Example:

		CORS_ORIGIN_WHITELIST = (
			'google.com',
			'hostname.example.com'
		)


	Default:

		CORS_ORIGIN_WHITELIST = ()


>CORS\_PREFLIGHT\_MAX\_AGE: specify the number of seconds a client/browser can cache the preflight response

	Note: A preflight request is an extra request that is made when making a "not-so-simple" request (eg. content-type is not application/x-www-form-urlencoded) to determine what requests the server actually accepts. Read more about it here: [http://www.html5rocks.com/en/tutorials/cors/](http://www.html5rocks.com/en/tutorials/cors/)

	Default:

		CORS_PREFLIGHT_MAX_AGE = 86400

>CORS\_ALLOW\_CREDENTIALS: specify whether or not cookies are allowed to be included in cross-site HTTP requests (CORS).

	Default:

		CORS_ALLOW_CREDENTIALS = False

## Changelog ##
v0.04 - add Access-Control-Allow-Credentials control to simple requests
v0.03 - bugfix (repair mismatched default variable names)
v0.02 - refactor/pull defaults into separate file
v0.01 - initial release
