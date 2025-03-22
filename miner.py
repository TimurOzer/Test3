import socket
import json
import hashlib
from datetime import datetime
import os

def calculate_alpha_hash(data):
    """Verilen veriyi SHA-256 ile hash'ler."""
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()

def connect_as_miner(host='192.168.1.106', port=12346):
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Miner socket created.")

        # Connect to the server
        print(f"Connecting to pool server at {host}:{port}...")
        client_socket.connect((host, port))
        print(f"Connected to pool server at {host}:{port}.")

        # Send the role to the server
        client_socket.send("miner".encode('utf-8'))

        while True:
            # Receive data from the server
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                # If no data is received, the server has disconnected
                print("Server disconnected.")
                break

            # Parse the received data as JSON
            try:
                file_data = json.loads(data)
                print(f"Received file data: {file_data}")

                # Add new fields to the data
                file_data["Alpha Signature"] = calculate_alpha_hash(file_data)  # Yeni imza
                file_data["Metadata"] = {}  # Metadata şimdilik boş
                file_data["Fee"] = 0  # Fee şimdilik 0
                file_data["Alpha Hash"] = calculate_alpha_hash(file_data)  # Yeni hash

                # Save the updated data to the miner/completed_transactions folder
                if not os.path.exists('miner/completed_transactions'):
                    os.makedirs('miner/completed_transactions')
                file_name = f"miner/completed_transactions/airdrop_{file_data['Sender']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                with open(file_name, 'w') as f:
                    json.dump(file_data, f, indent=4)
                print(f"Updated file data saved to {file_name}")

            except json.JSONDecodeError:
                print(f"Received non-JSON data: {data}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        client_socket.close()
        print("Miner socket closed.")

if __name__ == "__main__":
    connect_as_miner()