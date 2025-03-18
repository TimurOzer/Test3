import socket

def send_message_to_server(host='127.0.0.1', port=12345):  # Use '127.0.0.1' for localhost
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Client socket created.")
        
        # Connect to the server
        print(f"Attempting to connect to server at {host}:{port}...")
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}.")
        
        while True:
            # Get input from the user
            message = input("Enter your message (or type 'exit' to quit): ")
            if message.lower() == 'exit':
                # If the user types 'exit', close the connection
                print("Closing the connection...")
                break
            
            # Send the message to the server
            client_socket.send(message.encode('utf-8'))
            
            # Receive a response from the server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Response from server: {response}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        client_socket.close()
        print("Client socket closed.")

if __name__ == "__main__":
    send_message_to_server()