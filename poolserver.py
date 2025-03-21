import os
import socket
import threading

# Global variables
validators = 0
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
            validators += 1
        elif role == 'miner':
            miners += 1
        print(f"Total validators: {validators}, Total miners: {miners}")

    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                # If no data is received, the client has disconnected
                break
            print(f"Received from {client_address} ({role}): {data}")

            # Send a response back to the client
            client_socket.send("Message received!".encode('utf-8'))
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        # Close the connection
        client_socket.close()
        with connected_clients_lock:
            if role == 'validator':
                validators -= 1
            elif role == 'miner':
                miners -= 1
            print(f"Client {client_address} ({role}) disconnected.")
            print(f"Total validators: {validators}, Total miners: {miners}")

def start_pool_server(host='0.0.0.0', port=12346):
    # Create the 'pool' directory if it doesn't exist
    if not os.path.exists('pool'):
        os.makedirs('pool')
        print("'pool' directory created.")
    else:
        print("'pool' directory already exists.")

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Pool server socket created.")

    # Bind the socket to the address and port
    server_socket.bind((host, port))
    print(f"Pool server bound to {host}:{port}.")

    # Listen for incoming connections (max 5 clients in the waiting queue)
    server_socket.listen(5)
    print(f"Pool server is listening on {host}:{port}...")

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