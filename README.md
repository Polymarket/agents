# Agents

Trade autonomously on Polymarket using AI Agents.

## How to start?

1) Clone this repo
2) Add your OpenAI key and wallet to `.env`
3) Run this repo as:
    * command line `cli.py`
    * cron job `jobs/scheduler.py`
    * server (coming soon)

`lib/trade.py` contains core business logic which:
- queries polymarket data using the clob sdk
- performs rag using langchain and openai
- applies custom prompts in `ai/llm/prompts.py`
- automatically executes trades from your wallet

`lib/create.py` contains similar logic for creating markets.

## Customization

This tool is meant to be modular and extensible.

Below are instructions to begin developing on the codebase.

We welcome contributions and hope for this to be a community led project.

# Development

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
