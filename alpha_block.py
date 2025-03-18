import os
import json
from datetime import datetime

def create_alpha_block(prev_alpha_hash):
    # Define the alpha block structure
    alpha_block = {
        "Prev_Alpha_Hash": prev_alpha_hash,  # Previous Alpha Hash
        "Tag": "",  # Tag for the block
        "Timestamp": datetime.utcnow().isoformat(),  # Current timestamp
        "Sender": "",  # Sender of the block
        "Receiver": "",  # Receiver of the block
        "Chain Version": "",  # Chain version
        "Signature": "",  # Signature
        "Block Index": 0,  # Block index (will be incremented)
        "Metadata": {},  # Metadata
        "Smart Contract": "",  # Smart contract
        "Fee": "",  # Fee
        "Status": "",  # Status
        "Network": "",  # Network
        "Alpha Hash": ""  # Alpha Hash (will be calculated later)
    }

    # Ensure the 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Find the next available alpha block file name
    block_index = 1
    while os.path.exists(f'data/alpha{block_index}.json'):
        block_index += 1

    # Set the block index
    alpha_block["Block Index"] = block_index

    # Save the alpha block to a JSON file
    file_name = f'data/alpha{block_index}.json'
    with open(file_name, 'w') as f:
        json.dump(alpha_block, f, indent=4)

    print(f"Alpha block {block_index} created and saved to '{file_name}'.")

if __name__ == "__main__":
    # For testing, pass an empty previous Alpha Hash
    create_alpha_block("")