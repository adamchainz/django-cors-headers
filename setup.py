from setuptools import setup

setup(
    name='django-cors-headers',
    version='0.12',
    description='django-cors-headers is a Django application for handling the server headers required for Cross-Origin Resource Sharing (CORS).',
    author='Otto Yiu',
    author_email='otto@live.ca',
    url='https://github.com/ottoyiu/django-cors-headers',
    packages=['corsheaders'],
    license='MIT License',
    keywords='django cors middleware rest api',
    platforms = ['any'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['Django >= 1.4'],
    tests_require=['mock >= 1.0'],
    test_suite='tests.main',
)
