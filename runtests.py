#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys

import pytest


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    return pytest.main()


if __name__ == '__main__':
    sys.exit(main())
