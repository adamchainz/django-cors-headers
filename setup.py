from corsheaders import __version__
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    name='django-cors-headers',
    version=__version__,
    description='django-cors-headers is a Django application for handling the server headers required for Cross-Origin Resource Sharing (CORS).',
    long_description=readme + '\n\n' + history,
    author='Otto Yiu',
    author_email='otto@live.ca',
    url='https://github.com/ottoyiu/django-cors-headers',
    packages=['corsheaders'],
    license='MIT License',
    keywords='django cors middleware rest api',
    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[],
    tests_require=['mock >= 1.0'],
    test_suite='tests.main',
)
