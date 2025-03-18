import socket
import threading
import os  # Import the os module to handle directory creation

# Counter to keep track of connected clients
connected_clients = 0
connected_clients_lock = threading.Lock()  # Lock to ensure thread-safe updates

def handle_client(client_socket, client_address):
    global connected_clients
    print(f"Connection established with {client_address}.")
    with connected_clients_lock:
        connected_clients += 1
        print(f"Total connected clients: {connected_clients}")
    
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                # If no data is received, the client has disconnected
                break
            print(f"Received from {client_address}: {data}")
            
            # Send a response back to the client
            client_socket.send("Message received!".encode('utf-8'))
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break
    
    # Close the connection
    client_socket.close()
    with connected_clients_lock:
        connected_clients -= 1
        print(f"Client {client_address} disconnected.")
        print(f"Total connected clients: {connected_clients}")

def start_server(host='0.0.0.0', port=12345):
    try:
        # Create the 'data' directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
            print("'data' directory created.")
        else:
            print("'data' directory already exists.")
        
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server socket created.")
        
        # Bind the socket to the address and port
        server_socket.bind((host, port))
        print(f"Server bound to {host}:{port}.")
        
        # Listen for incoming connections (max 5 clients in the waiting queue)
        server_socket.listen(5)
        print(f"Server is listening on {host}:{port}...")
        
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
        print("Server socket closed.")

if __name__ == "__main__":
    start_server()