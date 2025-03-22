import socket
import hashlib
import os
import sys
import time
import subprocess
import json

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

def send_message(s):
    while True:
        message = input("Enter your message (or type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        s.send(message.encode())
        print(s.recv(1024).decode())

def delete_wallet(s):
    if os.path.exists('wallet.json'):
        with open('wallet.json', 'r') as f:
            wallet_data = json.load(f)
            wallet_address = wallet_data.get('address')
        
        os.remove('wallet.json')
        print("Wallet deleted locally.")
        
        # Send delete request to server
        s.send(f"DELETE_WALLET {wallet_address}".encode())
        response = s.recv(1024).decode()
        print(response)
    else:
        print("No wallet found to delete.")

def load_wallet():
    if os.path.exists('wallet.json'):
        with open('wallet.json', 'r') as f:
            wallet_data = json.load(f)
        print("Existing wallet loaded successfully!")
        print(f"Address: {wallet_data['address']}")
        return wallet_data
    else:
        print("No existing wallet found.")
        return None

def create_user_credentials():
    if not os.path.exists('user_credentials.json'):
        username = input("Create a username: ").strip()
        password = input("Create a password: ").strip()
        credentials = {
            'username': username,
            'password': hashlib.sha256(password.encode()).hexdigest()  # Hash the password
        }
        with open('user_credentials.json', 'w') as f:
            json.dump(credentials, f, indent=4)
        print("User credentials created successfully!")
    else:
        print("User credentials already exist. Loading...")

def authenticate_user():
    if os.path.exists('user_credentials.json'):
        with open('user_credentials.json', 'r') as f:
            credentials = json.load(f)
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if username == credentials['username'] and hashed_password == credentials['password']:
            print("Authentication successful!")
            return True
        else:
            print("Invalid username or password.")
            return False
    else:
        print("No user credentials found. Please create a new user.")
        return False

def show_menu(s):
    while True:
        print("\n--- MENU ---")
        print("1. Create Wallet")
        print("2. Change Password")
        print("3. Balance")
        print("4. Transfer")
        print("5. Airdrop")
        print("6. Miner")
        print("7. Validator")
        print("8. Network")
        print("9. Delete Wallet")
        print("10. Version")
        print("11. Send Message")
        print("12. Exit")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            print("Create Wallet selected.")
            # Send wallet creation request to server
            s.send("CREATE_WALLET".encode())
            
            # Receive wallet data from server
            response = s.recv(4096).decode()
            
            try:
                wallet_data = json.loads(response)
                # Save wallet data to wallet.json in the current directory
                with open('wallet.json', 'w') as f:
                    json.dump(wallet_data, f, indent=4)
                print(f"Wallet created successfully!")
                print(f"Address: {wallet_data['address']}")
                print(f"Private Key: {wallet_data['private_key']}")
                print(f"Wallet data saved to wallet.json")
            except json.JSONDecodeError:
                print("Error: Invalid wallet data received from server")
        elif choice == "2":
            print("Change Password selected.")
            # Change Password logic here
        elif choice == "3":
            print("Balance selected.")
            if os.path.exists('wallet.json'):
                with open('wallet.json', 'r') as f:
                    wallet_data = json.load(f)
                wallet_address = wallet_data.get('address')
                # Send balance request to server
                s.send(f"BALANCE {wallet_address}".encode())
                # Receive balance from server
                response = s.recv(1024).decode()
                print(f"Your balance: {response} Baklava")
            else:
                print("No wallet found. Please create a wallet first.")
        elif choice == "4":
            print("Transfer selected.")
            # Transfer logic here
        elif choice == "5":
            print("Airdrop selected.")
            # Airdrop logic here
        elif choice == "6":
            print("Miner selected.")
            # Miner logic here
        elif choice == "7":
            print("Validator selected.")
            # Validator logic here
        elif choice == "8":
            print("Network selected.")
            # Network logic here
        elif choice == "9":
            print("Delete Wallet selected.")
            delete_wallet(s)
        elif choice == "10":
            print("Version selected.")
            # Version logic here
        elif choice == "11":
            print("Send Message selected.")
            send_message(s)
        elif choice == "12":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

def start_client(host='0.0.0.0', port=12345):
    try:
        # Create or load user credentials
        create_user_credentials()
        if not authenticate_user():
            print("Authentication failed. Exiting...")
            return

        # Load existing wallet if it exists
        wallet_data = load_wallet()

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
            show_menu(s)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    start_client(host='164.92.247.14', port=12345)