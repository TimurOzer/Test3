import os
import json
from datetime import datetime

def create_genesis_block():
    # Define the genesis block structure
    genesis_block = {
        "Alpha Hash": "",
        "Security Hash": "",
        "Tag": "",
        "Timestamp": datetime.utcnow().isoformat(),
        "Sender": "",
        "Receiver": "",
        "Chain Version": "",
        "Signature": "",
        "Block Index": 0,  # Genesis block has index 0
        "Metadata": {},
        "Smart Contract": "",
        "Status": "Active",
        "Network": "",
        "Baklava Address": "",
        "Baklava MaxSupply": "",
        "Baklava Mining Reserve": "",
        "Baklava Airdrop Reserve": ""
    }

    # Ensure the 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Save the genesis block to a JSON file
    with open('data/genesis_block.json', 'w') as f:
        json.dump(genesis_block, f, indent=4)

    print("Genesis block created and saved to 'data/genesis_block.json'.")

if __name__ == "__main__":
    create_genesis_block()