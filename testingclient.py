import pygame
import socket
import threading
import pickle
from birdgame import Bird
from birdgame import Spikes
from birdgame import Spike
import uuid

# Pygame settings
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
PLAYER_SIZE = 25

# Network settings
HOST = 'localhost'
PORT = 5555

unique_id = uuid.uuid4()
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Player class to keep track of each player's data
class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 50
        self.height = 50
        self.game_done = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Player instance (Client's own player)
player = Player(WIDTH // 2, HEIGHT // 2, (0, 128, 255))
spike = Spikes(300, 300)

# List of other players
other_players = []


# Function to receive data from the server (other players' positions)
def receive_data(client):
    global other_players
    while True:
        try:
            data = client.recv(4096)
            if data:
                # Unpickle the received data
                player_data = pickle.loads(data)
                found = False
                for other_player in other_players:
                    other_play = other_player[0]
                    other_player[2]['spikebottomx'] = player_data[2]['spikebottomx']
                    other_player[2]['spikebottomy'] = player_data[2]['spikebottomy']
                    other_player[1]['spiketopx'] = player_data[1]['spiketopx']
                    other_player[1]['spiketopy'] = player_data[1]['spiketopy']
                    if other_play['id'] == player_data[0]['id']:
                        other_play['x'] = player_data[0]['x']
                        other_play['y'] = player_data[0]['y']
                        other_play['game_done'] = player_data[0]['game_done']
                        found = True
                        break
                    
                if not found:
                    other_players.append(player_data)
                    other_players[-1][0]['bird'] = Bird(200,200)
                    print(f"{player_data}")
        except:
            break

# Function to send data to the server (Player's own coordinates)
def send_data(client):
    while True:
        player_data = [{'id': unique_id, 'x': player.x, 'y': player.y, 'game_done': player.game_done},{'spiketopx': 0, 'spiketopy': 0},{'spikebottomx': spike.rect.x, 'spikebottomy': spike.rect.y}]
        print(f"This is spike coordinates sent {spike.rect.x}, {spike.rect.y}")
        client.send(pickle.dumps(player_data))
        pygame.time.delay(25)

def main():
    other_playes = False
   
    # Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Start receiving data in a separate thread
    threading.Thread(target=receive_data, args=(client,)).start()
    #if not other_players:
   
    #else:
        #spike = Spikes(other_players[0][2]['spikebottomx'], other_players[0][2]['spikebottomy'])

    # Start sending data in a separate thread
    threading.Thread(target=send_data, args=(client,)).start()
    pygame.time.delay(500)
    # Game loop
    running = True
    if other_players:
        other_playes = True
    while running:
        #print(f"This is id {unique_id}")
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle player movement (using arrow keys)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            last_time_moved_left = pygame.time.get_ticks()
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5
        if keys[pygame.K_UP]:
            player.y -= 5
        if keys[pygame.K_DOWN]:
            player.y += 5

        # Draw the player's own character
        player.draw(screen)
        # Draw other players

        for other_player in other_players:
            other_play = other_player[0]
            #pygame.draw.rect(screen, (255, 0, 0), (other_player['x'], other_player['y'], player.width, player.height))
            #consider putting the .get() method to avoid ['bird'] keyerror
            print(f"This is other_player[0] {other_play}")
            other = other_play.get('bird', None)
            if other:
                other.update_pos(screen, other_play['x'], other_play['y'])
        #print(f"This is otherplayees {other_playes}")
        current_time = pygame.time.get_ticks()
        if other_playes:
            #print("it is being received")
            #print(f"This is spikebottomx: {other_players[0][2]['spikebottomx']}")
            #print(f"This is spikebottomy: {other_players[0][2]['spikebottomy']}")
            print(f"This is other players {other_players}")
            spike.update_pos(screen, other_players[0][2]['spikebottomx'], other_players[0][2]['spikebottomy'])

        else:
            #print(f"It is spawning")
            #print(f"This is spikebottomx: {spike.rect.x}")
            #print(f"Thus is spikebottomy: {spike.rect.y}")
            spike.move()
            spike.draw(screen)

        pygame.display.update()
        clock.tick(60)

    # Close the connection
    client.close()
    pygame.quit()

if __name__ == "__main__":
    main()
