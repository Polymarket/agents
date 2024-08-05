# Polymarket Agents

Polymarket Agents is an advanced developer framework and set of utilities for building AI agents for Polymarket. estimating outcomes in information market, or bots that can trade in Polymarkets.

This code is free and publicly available under MIT License open source license!

## Features

- Integration with Polymarket API
- AI agent utilities for prediction markets
- Local and remote RAG (Retrieval-Augmented Generation) support
- Data sourcing from betting services, news providers, and web search
- Comphrehensive LLM tools for prompt engineering

# Getting started

This repo is inteded for use with Python 3.9

1. Clone the repository

   ```
   git clone https://github.com/{username}/polymarket-agents.git`
   cd polymarket-agents
   ```

2. Create the virtual environment

   ```
   python -m venv venv
   ```

3. Activate the virtual environment

   - On Windows:

   ```
   venv\Scripts\activate
   ```

   - On macOS and Linux:

   ```
   source venv/bin/activate
   ```

4. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

5. Set up your environment variables:

   - Create a `.env` file in the project root directory
   - Add the following environment variables:

   ```
   POLYGON_WALLET_PRIVATE_KEY=""
   OPENAI_API_KEY=""
   ```

6. Load your wallet with USDC.

7. Trade! 

   ```
   python application/trade.py
   ```

## Architecture

The Polymarket Agents architecture features modular components that can be maintained and extended by individual community members.

### Connectors

Polymarket Agents connectors standardize data sources and order types.

- `Polymarket.py`: defines a Polymarket class that interacts with the Polymarket API to retrieve and manage market and event data, and to execute orders on the Polymarket DEX. It includes methods for API key initialization, market and event data retrieval, and trade execution. The file also provides utility functions for building and signing orders, as well as examples for testing API interactions.

- `Objects.py`: data models using Pydantic; representations for trades, markets, events, and related entities.

- `Chroma.py`: chroma DB for vectorizing news sources and other API data. Developers are able to add their own vector database implementations.

- `Gamma.py`: defines `GammaMarketClient` class, which interfaces with the Polymarket Gamma API to fetch and parse market and event data. Methods to retrieve current and tradable markets, as well as defined information on specific markets and events.

### Scripts

Files for managing your local environment, server set-up to run the application remotely, and cli for end-user commands.

`Cli.py` is the primary user interface for the repo. Users can run various commands to interact with the Polymarket API, retrieve relevant news articles, query local data, send data/prompts to LLMs, and execute trades in Polymarkets.

Commands should follow this format:

`python cli.py command_name [attribute value] [attribute value]`

Example:

`get_all_markets`
Retrieve and display a list of markets from Polymarket, sorted by volume.

```
python cli.py get_all_markets --limit <LIMIT> --sort-by <SORT_BY>
```

- limit: The number of markets to retrieve (default: 5).
- sort_by: The sorting criterion, either volume (default) or another valid attribute.

# Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

# Related Repos

- [py-clob-client](https://github.com/Polymarket/py-clob-client): Python client for the Polymarket CLOB
- [python-order-utils](https://github.com/Polymarket/python-order-utils): Python utilities to generate and sign orders from Polymarket's CLOB
- [Polymarket CLOB client](https://github.com/Polymarket/clob-client): Typescript client for Polymarket CLOB
- [Langchain](https://github.com/langchain-ai/langchain): Utility for building context-aware reasoning applications
- [Chroma](https://docs.trychroma.com/getting-started): Chroma is an AI-native open-source vector database

# Prediction markets reading

- Prediction Markets: Bottlenecks and the Next Major Unlocks, Mikey 0x: https://mirror.xyz/1kx.eth/jnQhA56Kx9p3RODKiGzqzHGGEODpbskivUUNdd7hwh0
- The promise and challenges of crypto + AI applications, Vitalik Buterin: https://vitalik.eth.limo/general/2024/01/30/cryptoai.html
- Superforecasting: How to Upgrade Your Company's Judgement, Schoemaker and Tetlock: https://hbr.org/2016/05/superforecasting-how-to-upgrade-your-companys-judgment

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# Contact

For any questions or inquiries, please contact name@polymarket.com.

Enjoy using the CLI application! If you encounter any issues, feel free to open an issue on the repository.
