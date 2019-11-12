#!/bin/sh
set -ex
export CUSTOM_COMPILE_COMMAND="./compile.sh"
python3.5 -m piptools compile  --generate-hashes -P 'Django>=1.11,<2.0' "$@" -o py35-django111.txt
python3.5 -m piptools compile  --generate-hashes -P 'Django>=2.0,<2.1' "$@" -o py35-django20.txt
python3.5 -m piptools compile  --generate-hashes -P 'Django>=2.1,<2.2' "$@" -o py35-django21.txt
python3.5 -m piptools compile  --generate-hashes -P 'Django>=2.2,<2.3' "$@" -o py35-django22.txt
python3.6 -m piptools compile  --generate-hashes -P 'Django>=1.11,<2.0' "$@" -o py36-django111.txt
python3.6 -m piptools compile  --generate-hashes -P 'Django>=2.0,<2.1' "$@" -o py36-django20.txt
python3.6 -m piptools compile  --generate-hashes -P 'Django>=2.1,<2.2' "$@" -o py36-django21.txt
python3.6 -m piptools compile  --generate-hashes -P 'Django>=2.2,<2.3' "$@" -o py36-django22.txt
python3.6 -m piptools compile  --generate-hashes -P 'Django>=3.0a1,<3.1' "$@" -o py36-django30.txt
python3.7 -m piptools compile  --generate-hashes -P 'Django>=1.11,<2.0' "$@" -o py37-django111.txt
python3.7 -m piptools compile  --generate-hashes -P 'Django>=2.0,<2.1' "$@" -o py37-django20.txt
python3.7 -m piptools compile  --generate-hashes -P 'Django>=2.1,<2.2' "$@" -o py37-django21.txt
python3.7 -m piptools compile  --generate-hashes -P 'Django>=2.2,<2.3' "$@" -o py37-django22.txt
python3.7 -m piptools compile  --generate-hashes -P 'Django>=3.0a1,<3.1' "$@" -o py37-django30.txt
python3.8 -m piptools compile  --generate-hashes -P 'Django>=3.0a1,<3.1' "$@" -o py38-django30.txt
