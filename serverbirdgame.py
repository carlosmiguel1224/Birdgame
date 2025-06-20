import socket
import threading
import pickle
from testing-ip.py import *


local_ip = get_local_ip()
# Server settings
HOST = local_ip  # Address to bind the server to (this can also be a public IP for online play) 
#Change this to public ip later
PORT = 5555  # Port number the server listens on
MAX_PLAYERS = 10  # Max number of clients the server can handle simultaneously
clients = []  # List of all connected clients

def handle_client(client, addr):
    print(f"New connection: {addr}")
    while True:
        try:
            data = client.recv(4096)  # Receive data from client (max 4096 bytes)
            if not data:
                break  # If no data is received, client has disconnected
            print(clients)
            
            player_data = pickle.loads(data)  # Deserialize data (unpickle) to get player position
            # Broadcast the player's data (coordinates) to all other connected clients
            broadcast(player_data, client)
        except:
            break  # If there is an error (e.g., client disconnects), break the loop

    # Remove client from the list and close the connection when the client disconnects
    clients.remove(client)
    client.close()

def broadcast(player_data, current_client):
    """Send player data (coordinates) to all clients except the current one."""
    for client in clients:
        if client != current_client:
            try:
                client.send(pickle.dumps(player_data))  # Serialize and send data to client
            except:
                clients.remove(client)  # If client is disconnected, remove it from the list

def start():
    """Start the server, accept client connections, and handle them."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    server.bind((HOST, PORT))  # Bind the server to the specified host and port
    server.listen(MAX_PLAYERS)  # Set the maximum number of clients to listen for
    print(f"Server started on {HOST}:{PORT}")

    # Accept incoming client connections
    while True:
        client, addr = server.accept()  # Accept a new client connection
        clients.append(client)  # Add the client to the list of connected clients

        # Start a new thread to handle the client's communication with the server
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    start()  # Start the server
