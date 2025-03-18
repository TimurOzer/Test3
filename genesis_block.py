import os
import json
from datetime import datetime
import hashlib

def calculate_hash(data):
    """Calculate SHA-256 hash of the given data."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def create_genesis_block():
    # Define the genesis block structure
    genesis_data = {
        "Tag": "Genesis",
        "Timestamp": datetime.utcnow().isoformat(),
        "Sender": "Server",
        "Receiver": "Baklava BlockChain",
        "Chain Version": "0.0.0.1",
        "Signature": "",
        "Block Index": 0,  # Genesis block has index 0
        "Metadata": {},
        "Smart Contract": "",
        "Status": "Active",
        "Network": "CevizNet",
        "Baklava Address": "bklvdc38569a110702c2fed1164021f0539df178",
        "Baklava MaxSupply": 100000000,
        "Baklava Mining Reserve": 80000000,
        "Baklava Airdrop Reserve": 20000000
    }

    # Calculate Alpha Hash (hash of the entire genesis block data)
    alpha_hash_data = json.dumps(genesis_data, sort_keys=True)
    genesis_data["Alpha Hash"] = calculate_hash(alpha_hash_data)

    # Calculate Security Hash (hash of the Alpha Hash)
    genesis_data["Security Hash"] = calculate_hash(genesis_data["Alpha Hash"])

    # Ensure the 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Save the genesis block to a JSON file
    with open('data/genesis_block.json', 'w') as f:
        json.dump(genesis_data, f, indent=4)

    print("Genesis block created and saved to 'data/genesis_block.json'.")

if __name__ == "__main__":
    create_genesis_block()