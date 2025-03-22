import socket
import json
import hashlib
from datetime import datetime
import os

# Validator configuration
VALIDATOR_NAME = "Validator_01"  # Validator adı (manuel olarak ayarlanabilir)
CHAIN_VERSION = "0.0.0.1"  # Chain versiyonu (manuel olarak ayarlanabilir)
NETWORK = "Ceviznet"  # Ağ adı

def calculate_security_hash(data):
    """Verilen veriyi SHA-256 ile hash'ler."""
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()

def connect_as_validator(host='192.168.1.106', port=12346):
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Validator socket created.")

        # Connect to the server
        print(f"Connecting to pool server at {host}:{port}...")
        client_socket.connect((host, port))
        print(f"Connected to pool server at {host}:{port}.")

        # Send the role to the server
        client_socket.send("validator".encode('utf-8'))

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

                # Process the file data
                processed_data = {
                    "Tag": "Airdrop",
                    "Priority": file_data.get("priority", "low"),
                    "Timestamp": datetime.now().isoformat(),
                    "Sender": file_data.get("wallet_address", "Unknown"),
                    "Receiver": "System",
                    "Chain Version": CHAIN_VERSION,
                    "Signature": calculate_security_hash(file_data),  # İmza hash'i
                    "Block Index": get_block_index_from_server(),  # Blok indeksi
                    "Freud Detection": 0,  # Airdrop olduğu için 0
                    "Smart Contract": "None",  # Şimdilik yok
                    "Prize": 0,  # Şimdilik 0
                    "Status": "Completed",
                    "Network": NETWORK,
                    "Validator": VALIDATOR_NAME,
                    "Security Hash": calculate_security_hash(file_data)  # Güvenlik hash'i

                }

                # Save the processed data to completed_transactions folder
                if not os.path.exists('completed_transactions'):
                    os.makedirs('completed_transactions')
                file_name = f"completed_transactions/airdrop_{file_data['wallet_address']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                with open(file_name, 'w') as f:
                    json.dump(processed_data, f, indent=4)
                print(f"Processed data saved to {file_name}")

                # Send the processed data back to the pool server
                client_socket.send(json.dumps(processed_data).encode('utf-8'))
                print("Processed data sent back to the pool server.")

            except json.JSONDecodeError:
                print(f"Received non-JSON data: {data}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        client_socket.close()
        print("Validator socket closed.")

def get_block_index_from_server():
    """Server'dan blok indeksini alır (şimdilik manuel olarak 1 döndürüyor)."""
    # Bu kısımda server.py ile iletişim kurulabilir.
    # Şimdilik manuel olarak 1 döndürüyoruz.
    return 1

if __name__ == "__main__":
    connect_as_validator()