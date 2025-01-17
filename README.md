# Token-Sniper-Base

Token-Sniper-Base is a Python script that detects newly created ERC-20 tokens on the Base network and monitors liquidity on a decentralized exchange (DEX). The script uses Web3.py to interact with the blockchain and performs token detection and liquidity checks concurrently using threading.

## Features
- Detects newly created ERC-20 tokens on the Base network.
- Monitors liquidity for newly detected tokens on a decentralized exchange (DEX).
- Uses Uniswap-like factory and pair contracts to check liquidity for token pairs.
- Runs concurrently with Python threads for token detection and liquidity checks.

## Requirements
- Python 3.x
- [Web3.py](https://web3py.readthedocs.io/en/stable/) (Python library for interacting with Ethereum-compatible networks)
- threading (part of Python standard library)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Erald12/Token-Sniper-Base.git

2. Navigate to the project directory:

   '''bash
   cd Token-Sniper-Base

3. Install the required dependencies:
   pip install -r requirements.txt
   
   If requirements.txt does not exist, you can manually install the dependency using:
   pip install web3

Setup:
1. Replace BASE_RPC_URL with the URL of your Base network's RPC provider:
   BASE_RPC_URL = "https://mainnet.base.org"  # Your RPC URL here

2. The script is configured to monitor common token pairs (WETH, USDT) on the Ethereum mainnet. You can adjust this list or add other token addresses in the common_tokens list.
3. Modify the block range or adjust the scanning frequency if necessary.

Running the Script
To start monitoring new token creations and liquidity checks, run the following command:
python token_sniper_base.py

The script will continuously monitor the latest blocks for new tokens and check liquidity on the DEX.

Stopping the Script
To stop the script, press Ctrl + C to send a KeyboardInterrupt.

How It Works
Detecting New Tokens: The script checks the latest blocks for contract creation transactions (where the to address is None). If a new token is detected, its address is added to a list for further monitoring.

Checking Liquidity: The script checks if the newly detected tokens have liquidity on a DEX. It does this by interacting with the DEX's factory contract to find the pair for common tokens (like WETH and USDT) and checks the liquidity reserves.

Concurrency: The script uses Python's threading to run token detection and liquidity monitoring concurrently, enabling efficient real-time monitoring of the network.

Contributing
Contributions are welcome! Feel free to submit issues, pull requests, or suggestions.

License
This project is licensed under the MIT License. See the LICENSE file for details.
This `README.md` provides a detailed guide to setting up, running, and understanding your project. Make sure to replace `https://github.com/Erald12/Token-Sniper-Base.git` with the actual URL of your repository.
