# Agents

Please see `CONTRIBUTING.md` for contributing guidlines.

## Local Development

This repo is inteded for use with Python 3.9

```
virtualenv --python=python3.9 .venv
source .venv/bin/activate
```

## Docker Development

Run the following commands from the agents directory to run an ephemeral docker container with a bash shell and mounted volume:

```
./scripts/bash/build-docker.sh
./scripts/bash/run-docker-dev.sh
```
