import socket
import threading
import pickle
import copy
import sys
import os
import time
from testingip import *

local_ip = get_local_ip()
# Server settings
HOST = local_ip  # Address to bind the server to (this can also be a public IP for online play) 
#Change this to public ip later
PORT = 5555  # Port number the server listens on
MAX_PLAYERS = 10  # Max number of clients the server can handle simultaneously

clients = []  # List of all connected clients
first_to_connect = False 
spikeinfo = []
client1id = ''
first_client = {}
first_has_been_removed = False
game_ended = {}

def handle_client(client, addr):
    global first_to_connect
    global spikeinfo
    global client1id
    global first_client
    global first_has_been_removed
    global game_ended
    print(f"New connection: {addr}")
    while True:
        try:
            data = client.recv(4096)  # Receive data from client (max 4096 bytes)
            if not data:
                break  # If no data is received, client has disconnected
            

            #print(f"This is first to connect {first_to_connect}")
            player_data = pickle.loads(data)  # Deserialize data (unpickle) to get player position
            #print(f"This is player_data before: {player_data}")
            first_client[client] = first_client.get(client, player_data[0]['id'])
            print(f"This is first_client[client]: {first_client[client]}, This is still sending {player_data}")
            if not first_to_connect:
                first_to_connect = True
                client1info = player_data
                client1id = client1info[0]['id']
                first_client[client] = player_data[0]['id']

            if client1id == player_data[0]['id']:
                spikeinfo = player_data[1:]
            #print(f"player_data")
            

            game_ended[player_data[0]['id']] = game_ended.get(player_data[0]['id'], player_data[0]['game_done'])

            player_data[2]['spikebottomx'] = spikeinfo[1]['spikebottomx']
            #print(player_data[2]['spikebottomx'])
            player_data[2]['spikebottomy'] = spikeinfo[1]['spikebottomy']
            player_data[1]['spiketopx'] = spikeinfo[0]['spiketopx']
            player_data[1]['spiketopy'] = spikeinfo[0]['spiketopy']
            # Broadcast the player's data (coordinates) to all other connected clients

            broadcast(player_data, client)
        except Exception as e:
            print(f"Error while handling client {addr}: {e}")
            break  # If there is an error (e.g., client disconnects), break the loop

    # Remove client from the list and close the connection when the client disconnects
    game_over = all(i for i in list(game_ended.values()))
    print(f"This is game_over {game_ended.values()}")
    clients.remove(client)
    client.close()
    print(f"Client has been removed")
    if client1id == first_client[client]:
        #print(f"This is client1id: {client1id}, This is first_client[client]: {first_client[client]}")
        if len(list(first_client)) > 1:
            first_has_been_removed = True
            element = list(first_client)[1]
            client1id = first_client[element]
            del first_client[client]
            print(f"First client has disconnected. This is game_over {game_over}, This is first_has_been_removed {first_has_been_removed}")
            if game_over and first_has_been_removed:
                #Trigger the programmatic restart
                #spikeinfo = [{'spiketopx': 1000, 'spiketopy': -50},{'spikebottomx': 500, 'spikebottomy': 200}]
                #first_to_connect = False
                restart_server()
            #print(f"This is new client1id: {client1id}, This is new first_client[element]: {first_client[element]}")
        elif len(list(first_client)) == 0:
            first_to_connect == False
        else:
            del first_client[client]
            first_to_connect == False
    #print(len(list(first_client)))
    #print(first_client)

    #client.close()

def broadcast(player_data, current_client):
    """Send player data (coordinates) to all clients except the current one."""
    for client in clients:
        if client != current_client:
            try:
                client.send(pickle.dumps(player_data))  # Serialize and send data to client
            except Exception as e:
                print(f"Error while handling client {addr}: {e}")
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

def restart_server():
        """Programmatically restart the server."""
        # Perform any necessary cleanup
        print("Cleaning up before restart...")
        
        # Restart the server
        python = sys.executable
        script = sys.argv[0]
        os.execl(python, python, script)



if __name__ == "__main__":
    start()  # Start the server

