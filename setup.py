import os
import re

from setuptools import setup


def get_version(filename):
    with open(filename, "r") as fp:
        contents = fp.read()
    return re.search(r"__version__ = ['\"]([^'\"]+)['\"]", contents).group(1)


version = get_version(os.path.join("corsheaders", "__init__.py"))

with open("README.rst", "r") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", "r") as history_file:
    history = history_file.read()

setup(
    name="django-cors-headers",
    version=version,
    description=(
        "django-cors-headers is a Django application for handling the server "
        "headers required for Cross-Origin Resource Sharing (CORS)."
    ),
    long_description=readme + "\n\n" + history,
    author="Otto Yiu",
    author_email="otto@live.ca",
    maintainer="Adam Johnson",
    maintainer_email="me@adamj.eu",
    url="https://github.com/adamchainz/django-cors-headers",
    project_urls={
        "Changelog": (
            "https://github.com/adamchainz/django-cors-headers"
            + "/blob/master/HISTORY.rst"
        )
    },
    packages=["corsheaders"],
    license="MIT License",
    keywords=["django", "cors", "middleware", "rest", "api"],
    install_requires=["Django>=1.11"],
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
