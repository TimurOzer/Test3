import socket
import threading
import os
import hashlib
import genesis_block  # Import the genesis_block module
import wallet
import json

connected_clients = 0
connected_clients_lock = threading.Lock()

def get_server_client_hash():
    try:
        with open('client.py', 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        return None

def handle_client(client_socket, client_address):
    global connected_clients
    print(f"Connection established with {client_address}.")
    with connected_clients_lock:
        connected_clients += 1
        print(f"Total connected clients: {connected_clients}")

    try:
        data = client_socket.recv(1024).decode()
        if not data.startswith('HASH '):
            print("Invalid client protocol")
            return

        client_hash = data.split(' ')[1]
        server_hash = get_server_client_hash()

        if server_hash is None:
            client_socket.send(b'ERROR')
            return

        if client_hash != server_hash:
            print(f"{client_address} requires an update...")
            client_socket.send(b'UPDATE_AVAILABLE')
            with open('client.py', 'rb') as f:
                client_socket.sendall(f.read())
            print("Update sent!")
        else:
            client_socket.send(b'UP_TO_DATE')
            print(f"{client_address} is up to date.")
            while True:
                data = client_socket.recv(1024).decode()
                if not data or data.lower() == 'exit':
                    break
                # Handle wallet creation
                if data == "CREATE_WALLET":
                    print(f"{client_address} requested wallet creation")
                    # Create a wallet using wallet.py
                    new_wallet = wallet.create_wallet()
                    # Send wallet data back to client
                    client_socket.send(json.dumps(new_wallet).encode())
                # Handle balance request
                elif data.startswith("BALANCE"):
                    wallet_address = data.split(' ')[1]
                    wallet_file = f"wallets/{wallet_address}.json"
                    if os.path.exists(wallet_file):
                        with open(wallet_file, 'r') as f:
                            wallet_data = json.load(f)
                        # Get Baklava balance from tokens
                        baklava_balance = wallet_data.get('tokens', {}).get('Baklava', 0)
                        client_socket.send(str(baklava_balance).encode())
                    else:
                        client_socket.send("0".encode())  # Wallet not found, balance is 0
                # Handle delete wallet
                elif data.startswith("DELETE_WALLET"):
                    wallet_address = data.split(' ')[1]
                    if os.path.exists(f'wallets/{wallet_address}.json'):
                        os.remove(f'wallets/{wallet_address}.json')
                        client_socket.send(f"Wallet {wallet_address} deleted successfully.".encode())
                    else:
                        client_socket.send(f"Wallet {wallet_address} not found.".encode())
                else:
                    print(f"{client_address}: {data}")
                    client_socket.send("Message received!".encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        with connected_clients_lock:
            connected_clients -= 1
            print(f"{client_address} disconnected. Total connected clients: {connected_clients}")

def start_server(host='0.0.0.0', port=12345):
    # Create the genesis block if it doesn't exist
    if not os.path.exists('data/genesis_block.json'):
        genesis_block.create_genesis_block()

    #if not os.path.exists('client.py'):
    #    print("ERROR: client.py not found!")
    #    return

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()