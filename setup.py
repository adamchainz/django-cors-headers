from setuptools import setup

setup(
    name='django-cors-headers',
    version='0.06',
    description='Django app for handling the server headers required for Cross-Origin Resource Sharing (CORS).',
    author='Otto Yiu',
    author_email='otto@live.ca',
    url='https://github.com/OttoYiu/django-cors-headers',
    packages=['corsheaders'],
    install_requires=['Django >= 1.4'],
    tests_require=['mock >= 1.0'],
    test_suite='tests.main',
)
