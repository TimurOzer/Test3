import os
import json
import secrets
import hashlib

# Baklava address
BAKLAVA_ADDRESS = "bklvdc38569a110702c2fed1164021f0539df178"

def generate_private_key():
    """Generate a secure private key using secrets."""
    return secrets.token_hex(32)  # 32 bytes = 64 characters

def generate_address(private_key):
    """Generate a wallet address using SHA-256 hash of the private key."""
    return hashlib.sha256(private_key.encode('utf-8')).hexdigest()

def create_wallet():
    """Create a new wallet with a private key, address, token amounts, and Baklava address."""
    # Generate private key and address
    private_key = generate_private_key()
    address = generate_address(private_key)

    # Create wallet data with token amounts
    wallet = {
        "private_key": private_key,
        "address": address,
        "tokens": {
            "Baklava": 0,  # Initial amount of Baklava tokens
            # Other tokens can be added dynamically in the future
        },
        "metadata": {},  # Empty metadata
        "baklava_address": BAKLAVA_ADDRESS
    }

    # Ensure the 'wallets' directory exists
    if not os.path.exists('wallets'):
        os.makedirs('wallets')

    # Save the wallet to a JSON file
    wallet_file = f"wallets/{address}.json"
    with open(wallet_file, 'w') as f:
        json.dump(wallet, f, indent=4)

    print(f"Wallet created and saved to '{wallet_file}'.")
    return wallet

def add_token_to_all_wallets(token_name, initial_amount=0):
    """Add a new token to all existing wallets."""
    if not os.path.exists('wallets'):
        print("No wallets found. Create a wallet first.")
        return

    # Iterate over all wallet files in the 'wallets' directory
    for wallet_file in os.listdir('wallets'):
        if wallet_file.endswith('.json'):
            wallet_path = os.path.join('wallets', wallet_file)

            # Load the wallet
            with open(wallet_path, 'r') as f:
                wallet = json.load(f)

            # Add the new token if it doesn't already exist
            if token_name not in wallet["tokens"]:
                wallet["tokens"][token_name] = initial_amount
                print(f"Token '{token_name}' added to wallet {wallet['address']} with initial amount {initial_amount}.")

            # Save the updated wallet
            with open(wallet_path, 'w') as f:
                json.dump(wallet, f, indent=4)

if __name__ == "__main__":
    # Create a new wallet
    wallet = create_wallet()

    # Print wallet details
    print("\nWallet Details:")
    print(json.dumps(wallet, indent=4))

    # Example: Add a new token to all wallets (this can be done later)
    # add_token_to_all_wallets("NewToken", initial_amount=0)