import os
import json
from datetime import datetime

def create_security_block(prev_security_hash):
    # Define the security block structure
    security_block = {
        "Prev_Security_Hash": prev_security_hash,  # Previous Security Hash
        "Tag": "",  # Tag for the block
        "Timestamp": datetime.utcnow().isoformat(),  # Current timestamp
        "Sender": "",  # Sender of the block
        "Receiver": "",  # Receiver of the block
        "Chain Version": "",  # Chain version
        "Signature": "",  # Signature
        "Block Index": 0,  # Block index (will be incremented)
        "Freud Detection": "",  # Freud Detection
        "Validator": "",  # Validator
        "Smart Contract": "",  # Smart contract
        "Prize": "",  # Prize
        "Status": "",  # Status
        "Network": "",  # Network
        "Priority": "",  # Priority
        "Security Hash": ""  # Security Hash (will be calculated later)
    }

    # Ensure the 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Find the next available security block file name
    block_index = 1
    while os.path.exists(f'data/security{block_index}.json'):
        block_index += 1

    # Set the block index
    security_block["Block Index"] = block_index

    # Save the security block to a JSON file
    file_name = f'data/security{block_index}.json'
    with open(file_name, 'w') as f:
        json.dump(security_block, f, indent=4)

    print(f"Security block {block_index} created and saved to '{file_name}'.")

if __name__ == "__main__":
    # For testing, pass an empty previous Security Hash
    create_security_block("")