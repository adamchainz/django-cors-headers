#!/usr/bin/env python
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    os.environ["CUSTOM_COMPILE_COMMAND"] = "requirements/compile.py"
    os.environ["PIP_REQUIRE_VIRTUALENV"] = "0"
    common_args = [
        "-m",
        "piptools",
        "compile",
        "--generate-hashes",
        "--allow-unsafe",
    ] + sys.argv[1:]
    subprocess.run(
        [
            "python3.7",
            *common_args,
            "-P",
            "Django>=3.2a1,<3.3",
            "-o",
            "py37-django32.txt",
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "python3.8",
            *common_args,
            "-P",
            "Django>=3.2a1,<3.3",
            "-o",
            "py38-django32.txt",
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "python3.8",
            *common_args,
            "-P",
            "Django>=4.0a1,<4.1",
            "-o",
            "py38-django40.txt",
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "python3.9",
            *common_args,
            "-P",
            "Django>=3.2a1,<3.3",
            "-o",
            "py39-django32.txt",
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "python3.9",
            *common_args,
            "-P",
            "Django>=4.0a1,<4.1",
            "-o",
            "py39-django40.txt",
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "python3.10",
            *common_args,
            "-P",
            "Django>=3.2a1,<3.3",
            "-o",
            "py310-django32.txt",
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "python3.10",
            *common_args,
            "-P",
            "Django>=4.0a1,<4.1",
            "-o",
            "py310-django40.txt",
        ],
        check=True,
        capture_output=True,
    )
