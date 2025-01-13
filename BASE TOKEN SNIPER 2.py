import threading
from web3 import Web3

# Replace this with your Base RPC URL
BASE_RPC_URL = "https://mainnet.base.org"

# Connect to the Base network
web3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))

# Check connection
if not web3.is_connected():
    print("Failed to connect to Base network.")
    exit()

print("Connected to Base network!")

# ERC-20 contract ABI (additional functions to detect minting and owner control)
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",  # Check if the contract has an owner address
        "outputs": [{"name": "", "type": "address"}],
        "type": "function",
    },
]

# DEX contract ABI (for Uniswap-like DEXes)
DEX_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "tokenA", "type": "address"},
            {"name": "tokenB", "type": "address"},
            {"name": "amountA", "type": "uint256"},
            {"name": "amountB", "type": "uint256"},
            {"name": "to", "type": "address"},
            {"name": "deadline", "type": "uint256"}
        ],
        "name": "addLiquidity",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
]

# Example Uniswap Factory Contract ABI (simplified for the function we need)
FACTORY_ABI = [
    {
        "constant": True,
        "inputs": [
            {"name": "tokenA", "type": "address"},
            {"name": "tokenB", "type": "address"}
        ],
        "name": "getPair",
        "outputs": [{"name": "", "type": "address"}],
        "type": "function",
    }
]

# The address of the DEX Factory contract
FACTORY_ADDRESS = web3.to_checksum_address("0x8909Dc15e40173Ff4699343b6eB8132c65e18eC6")


# Example Pair Contract ABI (simplified for the function we need)
PAIR_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "getReserves",
        "outputs": [{"name": "reserve0", "type": "uint256"}, {"name": "reserve1", "type": "uint256"}, {"name": "blockTimestampLast", "type": "uint256"}],
        "type": "function",
    }
]

# Define the new_tokens list outside the function
new_tokens = []

def detect_new_tokens():
    """
    Detects new token creations and monitors liquidity additions for new tokens.
    """
    global new_tokens

    while True:
        latest_block = web3.eth.block_number
        for block_number in range(latest_block - 5, latest_block + 1):
            block = web3.eth.get_block(block_number, full_transactions=True)
            for tx in block.transactions:
                if tx["to"] is None:  # Contract creation transactions have `to` set to None
                    try:
                        # Get the contract address (new token address)
                        receipt = web3.eth.get_transaction_receipt(tx["hash"])
                        contract_address = receipt["contractAddress"]

                        # Check if it's an ERC-20 token contract
                        contract = web3.eth.contract(address=contract_address, abi=ERC20_ABI)
                        token_name = contract.functions.name().call()
                        token_symbol = contract.functions.symbol().call()

                        # If it's a valid token, store its address
                        #print(f"New Token Detected: {token_name} ({token_symbol}) at {contract_address}")
                        new_tokens.append(contract_address)

                    except Exception as e:
                        # Skip if the contract doesn't match ERC-20 standard or fails
                        pass


def check_liquidity_on_dex():
    """
    Checks if the newly detected tokens have liquidity on a DEX using the factory contract.
    """
    while True:
        if len(new_tokens) > 0:
            for token_address in new_tokens:
                # Convert token address to checksum format
                token_address = web3.to_checksum_address(token_address)

                # Interact with the DEX Factory contract
                factory_contract = web3.eth.contract(address=FACTORY_ADDRESS, abi=FACTORY_ABI)

                # Loop over common trading pairs
                common_tokens = [
                    web3.to_checksum_address("0x4200000000000000000000000000000000000006"),  # WETH address on Ethereum Mainnet
                    web3.to_checksum_address("0xdac17f958d2ee523a2206206994597c13d831ec7")  # USDT address on Ethereum Mainnet
                ]

                for common_token in common_tokens:
                    try:
                        # Get the pair address for the current token and the common token (ETH or USDT)
                        pair_address = factory_contract.functions.getPair(token_address, common_token).call()

                        if pair_address != "0x0000000000000000000000000000000000000000":
                            # If a pair exists, check liquidity in the pair
                            pair_contract = web3.eth.contract(address=pair_address, abi=PAIR_ABI)
                            reserves = pair_contract.functions.getReserves().call()

                            reserve_tokenA, reserve_tokenB, _ = reserves
                            liquidity = reserve_tokenA if token_address != common_token else reserve_tokenB

                            if liquidity > 0:
                                token = web3.eth.contract(address=token_address, abi=ERC20_ABI)
                                token_name = token.functions.name().call()
                                print(f"Liquidity found for token '{token_name}' - CA: {token_address}")
                                new_tokens.remove(token_address)  # Remove token_address from new_tokens

                    except Exception as e:
                        continue

def run_detection():
    latest_block = web3.eth.block_number
    blocks_to_scan = 5  # Adjust as needed

    # Start both functions concurrently in separate threads
    thread1 = threading.Thread(target=detect_new_tokens)
    thread2 = threading.Thread(target=check_liquidity_on_dex)

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for threads to finish (they will run forever in this case)
    thread1.join()
    thread2.join()


try:
    run_detection()

except KeyboardInterrupt:
    print("Monitoring stopped.")
