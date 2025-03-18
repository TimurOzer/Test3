import socket
import hashlib
import os
import sys
import time
import subprocess

def get_current_hash():
    with open(__file__, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def update_client(new_data):
    with open(__file__, 'wb') as f:
        f.write(new_data)
    print("Update completed! Restarting the client...")
    # Restart the client using subprocess
    subprocess.Popen([sys.executable, __file__])
    sys.exit(0)  # Close the current instance

def start_client(host='127.0.0.1', port=12345):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        current_hash = get_current_hash()
        s.send(f'HASH {current_hash}'.encode())
        
        response = s.recv(1024)
        if response.startswith(b'UPDATE_AVAILABLE'):
            print("A new update is available!")
            user_input = input("Do you want to update? (yes/no): ").strip().lower()
            if user_input == 'yes':
                data = response[len(b'UPDATE_AVAILABLE'):]
                while True:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                update_client(data)
                return
            else:
                print("Update declined. Your version is not up to date.")
                print("The application will close in 5 seconds...")
                time.sleep(5)
                sys.exit(0)
        
        elif response == b'UP_TO_DATE':
            print("Client is up to date!")
            while True:
                message = input("Enter your message (or type 'exit' to quit): ")
                if message.lower() == 'exit':
                    break
                s.send(message.encode())
                print(s.recv(1024).decode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    start_client()