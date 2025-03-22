import os
import socket
import threading
import random
import json
import time
from datetime import datetime

# Global variables
validators = []
miners = 0
connected_clients_lock = threading.Lock()

def handle_client(client_socket, client_address):
    global validators, miners

    # Receive the role from the client (validator or miner)
    role = client_socket.recv(1024).decode('utf-8').strip().lower()
    if role not in ['validator', 'miner']:
        print(f"Invalid role from {client_address}. Closing connection.")
        client_socket.close()
        return

    print(f"New connection from {client_address} as {role}.")
    with connected_clients_lock:
        if role == 'validator':
            validators.append(client_socket)  # Add validator socket to the list
        elif role == 'miner':
            miners += 1
        print(f"Total validators: {len(validators)}, Total miners: {miners}")

    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                # If no data is received, the client has disconnected
                break

            # Check if the data is processed airdrop data from a validator
            try:
                processed_data = json.loads(data)
                if "Tag" in processed_data and processed_data["Tag"] == "Airdrop":
                    # Save the processed data to the pool/miner folder
                    if not os.path.exists('pool/miner'):
                        os.makedirs('pool/miner')
                    file_name = f"pool/miner/airdrop_{processed_data['Sender']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                    try:
                        with open(file_name, 'w') as f:
                            json.dump(processed_data, f, indent=4)
                        print(f"Processed airdrop data saved to {file_name}")
                    except PermissionError:
                        print(f"Permission denied: Unable to save {file_name}.")
                    except Exception as e:
                        print(f"Error saving {file_name}: {e}")
            except json.JSONDecodeError:
                print(f"Received non-JSON data: {data}")

            # Send a response back to the client
            client_socket.send("Message received!".encode('utf-8'))
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        # Close the connection
        client_socket.close()
        with connected_clients_lock:
            if role == 'validator':
                validators.remove(client_socket)  # Remove validator socket from the list
            elif role == 'miner':
                miners -= 1
            print(f"Client {client_address} ({role}) disconnected.")
            print(f"Total validators: {len(validators)}, Total miners: {miners}")

def process_pool():
    while True:
        try:
            # Check the pool/validator directory for files
            if os.path.exists('pool/validator'):
                pool_files = os.listdir('pool/validator')
                pool_files.sort()  # Sort files by name (sequence number)

                if pool_files:
                    # Process the first file in the sorted list
                    file_name = pool_files[0]
                    file_path = os.path.join('pool/validator', file_name)

                    # Check if the file exists and is readable
                    if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
                        with open(file_path, 'r') as f:
                            file_data = json.load(f)

                        priority = file_data.get('priority', 'low')
                        sequence = file_data.get('sequence', 5)

                        print(f"Processing file: {file_name}, Priority: {priority}, Sequence: {sequence}")

                        # If priority is low and sequence is 5, send to a random validator
                        if priority == 'low' and sequence == 5:
                            if validators:
                                # Choose a random validator
                                validator_socket = random.choice(validators)
                                validator_socket.send(json.dumps(file_data).encode('utf-8'))
                                print(f"Sent {file_name} to a validator.")
                            else:
                                print("No validators available. Retrying later...")
                        else:
                            print(f"File {file_name} is not a low-priority airdrop. Skipping.")

                        # Remove the processed file
                        try:
                            os.remove(file_path)
                            print(f"Removed {file_name} from the pool/validator.")
                        except PermissionError:
                            print(f"Permission denied: Unable to remove {file_name}.")
                        except Exception as e:
                            print(f"Error removing {file_name}: {e}")
                    else:
                        print(f"File {file_name} is not accessible. Skipping.")
                else:
                    print("No files in the pool/validator. Waiting...")
            else:
                print("pool/validator directory does not exist. Creating...")
                os.makedirs('pool/validator')

            # Wait before checking the pool again
            time.sleep(5)
        except Exception as e:
            print(f"Error processing pool: {e}")

def start_pool_server(host='0.0.0.0', port=12346):
    # Create the 'pool' directory and subdirectories if they don't exist
    try:
        if not os.path.exists('pool'):
            os.makedirs('pool')
            print("'pool' directory created.")
        if not os.path.exists('pool/validator'):
            os.makedirs('pool/validator')
            print("'pool/validator' directory created.")
        if not os.path.exists('pool/miner'):
            os.makedirs('pool/miner')
            print("'pool/miner' directory created.")
        else:
            print("'pool' directory and subdirectories already exist.")
    except PermissionError:
        print("Permission denied: Unable to create directories. Check your permissions.")
        return
    except Exception as e:
        print(f"An error occurred while creating directories: {e}")
        return

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Pool server socket created.")

    # Bind the socket to the address and port
    server_socket.bind((host, port))
    print(f"Pool server bound to {host}:{port}.")

    # Listen for incoming connections (max 5 clients in the waiting queue)
    server_socket.listen(5)
    print(f"Pool server is listening on {host}:{port}...")

    # Start the pool processing thread
    pool_thread = threading.Thread(target=process_pool, daemon=True)
    pool_thread.start()

    try:
        while True:
            # Accept a connection from a client
            client_socket, client_address = server_socket.accept()

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the server socket
        server_socket.close()
        print("Pool server socket closed.")

if __name__ == "__main__":
    start_pool_server()