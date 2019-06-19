#!/usr/bin/env python
import os
import sys

import pytest


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    return pytest.main()


if __name__ == "__main__":
    sys.exit(main())
