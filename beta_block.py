import os
import json
from datetime import datetime

def create_beta_block(prev_security_hash, prev_alpha_hash):
    # Define the beta block structure
    beta_block = {
        "Prev_Security_Hash": prev_security_hash,  # Previous Security Hash
        "Prev_Alpha_Hash": prev_alpha_hash,  # Previous Alpha Hash
        "Signer": "",  # Signer of the block
        "Approve": "",  # Approval status
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
        "Prize": "",  # Prize
        "Status": "",  # Status
        "Network": "",  # Network
        "Security Hash": "",  # Security Hash (will be calculated later)
        "Alpha Hash": ""  # Alpha Hash (will be calculated later)
    }

    # Ensure the 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Find the next available beta block file name
    block_index = 1
    while os.path.exists(f'data/beta{block_index}.json'):
        block_index += 1

    # Set the block index
    beta_block["Block Index"] = block_index

    # Save the beta block to a JSON file
    file_name = f'data/beta{block_index}.json'
    with open(file_name, 'w') as f:
        json.dump(beta_block, f, indent=4)

    print(f"Beta block {block_index} created and saved to '{file_name}'.")

if __name__ == "__main__":
    # For testing, pass empty previous Security and Alpha Hashes
    create_beta_block("", "")