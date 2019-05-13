#!/bin/sh
set -ex
export CUSTOM_COMPILE_COMMAND="./requirements-compile.sh"
python3.5 -m piptools compile -P 'Django>=1.11,<2.0' "$@" -o requirements/py35-django111.txt
python3.5 -m piptools compile -P 'Django>=2.0,<2.1' "$@" -o requirements/py35-django20.txt
python3.5 -m piptools compile -P 'Django>=2.1,<2.2' "$@" -o requirements/py35-django21.txt
python3.5 -m piptools compile -P 'Django>=2.2,<2.3' "$@" -o requirements/py35-django22.txt
python3.6 -m piptools compile -P 'Django>=1.11,<2.0' "$@" -o requirements/py36-django111.txt
python3.6 -m piptools compile -P 'Django>=2.0,<2.1' "$@" -o requirements/py36-django20.txt
python3.6 -m piptools compile -P 'Django>=2.1,<2.2' "$@" -o requirements/py36-django21.txt
python3.6 -m piptools compile -P 'Django>=2.2,<2.3' "$@" -o requirements/py36-django22.txt
python3.7 -m piptools compile -P 'Django>=1.11,<2.0' "$@" -o requirements/py37-django111.txt
python3.7 -m piptools compile -P 'Django>=2.0,<2.1' "$@" -o requirements/py37-django20.txt
python3.7 -m piptools compile -P 'Django>=2.1,<2.2' "$@" -o requirements/py37-django21.txt
python3.7 -m piptools compile -P 'Django>=2.2,<2.3' "$@" -o requirements/py37-django22.txt
