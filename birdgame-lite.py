import random
import pygame
import sys
import time
import socket
import threading
import pickle
import uuid
import os
from testingip import *
# Initialize Pygame
pygame.init()

local_ip = get_local_ip()
# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30  # Frames per second
BIRD_COLOR = (255, 0, 0)
other_players = []
other_playes = False
reconnected_restart = False
# Network settings
HOST = local_ip
PORT = 5555

unique_id = uuid.uuid4()
# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bird Game")

fonts = pygame.font.get_fonts()
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DIRECTIONS = ["up","down", "left","right"]


background_image = pygame.image.load('bird_background.jpg')
# Optionally, scale the image to fit the screen
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

initialtext = pygame.image.load('Bird-Game.png')
presstoplay = pygame.image.load('Press-up-to-play-.png')

font = pygame.font.SysFont("chalkboard", 48)  # You can choose a different font and size
def displaytextfont(surface, x, y, text):
    surface.blit(text, (x,y))
def display_score(surface, score, x, y):
    text_surface = font.render(f"score:{score}", True, BLACK)  # Render the text
    surface.blit(text_surface, (x, y))
def displaytext(surface,text,x,y):
    text_surface = font.render(text, True, BLACK)
    surface.blit(text_surface,(x,y))
class Bird:
    def __init__(self, x, y, avatar= 'angry_bird.png'):
        self.rect = pygame.Rect(x, y, 50, 50)  # Create a rectangle for the bird
        self.speed = 2
        self.velocity_y = 0
        bird_image = pygame.image.load(avatar)  # Replace 'bird.png' with your image filename
        self.bird_image = pygame.transform.scale(bird_image, (50, 50))
        self.game_done = True


    def move(self):
        keys = pygame.key.get_pressed()
        # Apply gravity
        self.velocity_y += .5  # Increase velocity due to gravity
        self.rect.y += self.velocity_y  # Update vertical position

        # Jumping logic
        if keys[pygame.K_UP]:
            self.velocity_y = -10  # Set upward velocity when jumping

        # Prevent falling through the ground
        #if self.rect.y + self.rect.height > SCREEN_HEIGHT:
            #self.rect.y = SCREEN_HEIGHT - self.rect.height  # Reset to ground level
            #self.velocity_y = 0  # Stop downward movement

    def draw(self, surface):
        surface.blit(self.bird_image, (self.rect.x, self.rect.y))  # Draw the bird on the screen

    def update_pos(self,surface, x=0, y=0):
        self.rect.x = x
        self.rect.y = y
        surface.blit(self.bird_image, (x, y))

    def get_pos(self):
        return (self.rect.x , self.rect.y)
        
class Spikes:
    def __init__(self,x , y):
        self.rect = pygame.Rect(x , y, 100, 500)
        spike_image = pygame.image.load('pipe5.jpeg')
        self.spike_image = pygame.transform.scale(spike_image, (100, 500))
        self.speed = 6
    def move(self):
        self.rect.x -= self.speed
    def draw(self, screen):
        #print(f"This is spike position {self.rect}")
        if self.rect.right < 0:
            vary = random.randint(100,400)
            self.rect.topleft = (800,vary)   
        screen.blit(self.spike_image, (self.rect.x, self.rect.y))

    def update_pos(self,screen, x, y):
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.spike_image, (x, y))

class Spike(Spikes):
    def __init__(self, x, y):
        super().__init__(x,y,)
        self.spike_image = pygame.transform.rotate(self.spike_image, 180)

    def draw(self,screen, spikes):
        if self.rect.right < 0:
            vary = random.randint(-250,-50)
            if spikes.rect.x - self.rect.x > 900:
                #print(f"distance is bigger")
                varx = random.randint(SCREEN_WIDTH - spikes.rect.x , (SCREEN_WIDTH -spikes.rect.x ))
            elif spikes.rect.x - self.rect.x < 350:
                #print(f"distance is smaller")
                varx = random.randint(SCREEN_WIDTH-15, SCREEN_WIDTH)
            else:
                varx = random.randint(800,900)
            #print(f"This is where up is spawning {varx}")
            # (spikes.rect)%SCREEN_WIDTH + (self.rect.x)%SCREEN_WIDTH
            self.rect.topleft = (varx,vary)   
        screen.blit(self.spike_image, (self.rect.x, self.rect.y))

    def update_pos(self, screen, x, y):
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.spike_image, (x, y))
    
class Enemy:
    def __init__(self, x, y):
        self.bulletspeed = 2
        self.speed = 5
        self.available_directions = ["left","up"]
        bird_image = pygame.image.load('bluy.png')  # Replace 'bird.png' with your image filename
        bird_image = pygame.transform.scale(bird_image, (80, 50))
        self.bird_image = bird_image #pygame.transform.rotate(bird_image, 180)
        self.rect = pygame.Rect(x, y, 80, 50)
        self.direction = "right"

    def get_directions(self, spike, spikes):
        self.available_directions = []
        new_x, new_y = self.rect.x, self.rect.y
        new_rect = self.rect
        for i in DIRECTIONS:
            new_x, new_y = self.rect.x, self.rect.y 
            new_rect = self.rect
            if i == "up":
                new_y += 25
            elif i == "down":
                new_y -= 25
            elif i == "right":
                new_x += 25
            elif i == "left":
                new_x -= 150
            new_rect = pygame.Rect(new_x, new_y, 50, 50)
            #print(f"These are all of them: {i}")
            if not new_rect.colliderect(spike.rect) and not new_rect.colliderect(spikes.rect) and 0<= new_rect.x <= SCREEN_WIDTH and 0<= new_rect.y <= SCREEN_HEIGHT:
                #print(f"direction:{i}")
                self.available_directions.append(i)
            #random.shuffle(self.available_directions)
            print(f"This is self.rect{self.rect}")
            print(f"This is bottomspike pos{spike.rect}")
            print(f"This is topspike pos{spikes.rect}")
            print(f"These are availabledirections {self.available_directions}")
        return

    def opp(self,available_directions):
        opposite = ""
        ind = 0
        if available_directions:
            if self.direction == "right":
                opposite = "left"
            elif self.direction == "left":
                opposite = "right"
            elif self.direction == "up":
                opposite = "down"
            elif self.direction == "down":
                opposite = "up"
            for direction in available_directions:
                if direction == opposite:
                    break
                ind += 1
            if opposite in available_directions:
                available_directions.pop(ind)
            #print(f"this is ind: {ind}")
            available_directions.append(opposite)
        return

    def move(self, spike, spikes):
        self.get_directions(spike, spikes)
        self.opp(self.available_directions)
        #print(self.available_directions)
        #print(f"These are the optimal directions: {self.available_directions}")
        if self.available_directions:
            optimal_move = self.available_directions[0]
            if self.direction in self.available_directions and len(self.available_directions)<= 3:
                optimal_move = self.direction
            if optimal_move == "left":
                self.rect.x -= self.speed
                self.direction = "left"
            elif optimal_move == "right":
                self.rect.x += self.speed
                self.direction = "right"
            elif optimal_move == "up":
                self.rect.y += self.speed
                self.direction = "up"
            elif optimal_move == "down":
                self.rect.y -= self.speed
                self.direction = "down"
            print(f"This is direction {self.direction}")

    def draw(self, screen):
        screen.blit(self.bird_image, self.rect)

def score(bird, spike, spikes):
    socre = 0
    if bird.rect.centerx >= spike.rect.centerx or bird.rect.centerx >= spikes.rect.centerx:
        score += 1
    return score

def out_of_bounds(player):
    if player.rect.y > 800 or player.rect.y < -100:
        return True


def delay(current_time, time_of_delay):
    end_time = 0
    while (end_time - current_time) <= time_of_delay:
        end_time = pygame.time.get_ticks()
    return True

def restart_client():
    print("Restarting client due to a connection error...")
    time.sleep(1)  # Wait for 2 seconds before restarting (optional)
    python = sys.executable
    script = sys.argv[0]
    os.execl(python, python, script)


def reconnect(client):
    global reconnected_restart
    while True:
        #unique_id = uuid.uuid4()
        try:
            print("Attempting to reconnect to the server...")
            # Reconnect logic: create a new socket and reconnect
            new_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_client.connect((HOST, PORT))
            
            print("Reconnected to the server successfully.")
            
            # Restart receiving and sending threads
            threading.Thread(target=receive_data, args=(new_client,)).start()
            threading.Thread(target=send_data, args=(new_client,)).start()
            reconnected = True
            break  # Exit the reconnection loop once connected
        except Exception as e:
            print(f"Error reconnecting: {e}")
            time.sleep(3)  # Wait 5 seconds before retrying the connection



player = Bird(100,350, 'bluy.png')
spikebottom = Spikes(500,200)
spiketop = Spike(1000,-50)
# List of other players
other_players = []

# Function to receive data from the server (other players' positions)
def receive_data(client):
    global other_players
    global other_playes
    global reconnected_restart
    while True:
        try:
            data = client.recv(4096)
            if data:
                # Unpickle the received data
                player_data = pickle.loads(data)
                found = False
                #print(f"This is player_data {player_data}")
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
        except (BrokenPipeError, ConnectionResetError):
            restart_client()
            break
        except:
            break

# Function to send data to the server (Player's own coordinates)
def send_data(client):
    global other_players
    global other_playes
    while True:
        try:
            #print(f"I am sending these coordinates: {player.rect.x}, {player.rect.y}")
            player_data = [{'id': unique_id, 'x': player.rect.x, 'y': player.rect.y, 'game_done': player.game_done},{'spiketopx': spiketop.rect.x, 'spiketopy': spiketop.rect.y},{'spikebottomx': spikebottom.rect.x, 'spikebottomy': spikebottom.rect.y}]
            #print(spiketop.rect.x)
            client.send(pickle.dumps(player_data))
            pygame.time.delay(25)
        except (BrokenPipeError, ConnectionResetError):
            restart_client()
            break
        except:
            break

def main():
    #other_players = []
    print(f"This is my unique id {unique_id}")
    other_playes = False

    # Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Start receiving data in a separate thread
    threading.Thread(target=receive_data, args=(client,)).start()

    # Start sending data in a separate thread
    threading.Thread(target=send_data, args=(client,)).start()

    pygame.time.delay(3000)
    
    if other_players:
        other_playes = True
    running = True
    game_ended = False
    #score = 0
    show_text = True
    clock = pygame.time.Clock()
    #player = Bird(100,350)
    #spikebottom = Spikes(500,200)
    #spiketop = Spike(1000, -50)
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic goes here
            #if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_UP:  # Change this key to whatever you prefer
                    #gameover = False
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))
        #print(f"This is showtext val: {show_text}")
        if show_text:
            #player.game_done = False
            score = 0
            #player = Bird(100,350)
            #spikebottom = Spikes(500,200)
            #spiketop = Spike(1000,-50)
            #enemy = Enemy(650,300)
            displaytextfont(screen, 140, 80, initialtext)
            displaytextfont(screen, 190, 170, presstoplay)
            #print(f"This is player.game_done: {player.game_done}")
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:  # Start the game
                player.game_done = False
                show_text = False
        # Clear the screen
        else:
            print(f"player coordinates: {player.rect.y} ")
            game_ended = all(player[0]['game_done'] == True for player in other_players)
            #print(f"This is game ended {player.game_done}")
                # Drawing code goes here
            if player.rect.colliderect(spiketop.rect) or player.rect.colliderect(spikebottom.rect) or game_ended and player.game_done or out_of_bounds(player):
                player.game_done = True
                #We need to delay the show text until game_done == True all other_players
                player.update_pos(screen, 1000,3000)
                game_ended = all(player[0]['game_done'] == True for player in other_players)
                if game_ended and player.game_done:
                    pygame.time.delay(200)
                    spikebottom.update_pos(screen, 500,200)
                    spiketop.update_pos(screen, 1000, -50)
                    player.update_pos(screen, 100, 350)
                    show_text = True 
                    #player.game_done = False
            if spiketop.rect.centerx-2<= player.rect.centerx<= spiketop.rect.centerx+2 or spikebottom.rect.centerx-2 <= player.rect.centerx <= spikebottom.rect.centerx +2:
                score += 1
            display_score(screen, score, 0, 0)
            # Draw other players
            for other_player in other_players:
                other_play = other_player[0]
                #pygame.draw.rect(screen, (255, 0, 0), (other_player['x'], other_player['y'], player.width, player.height))
                #consider putting the .get() method to avoid ['bird'] keyerror

                other = other_play.get('bird', None)
                if other:
                    #print(f"This is other bird info {other_play['x']}, {other_play['y']}")
                    #other_play['x'] = 'hello'
                    other.update_pos(screen, other_play['x'], other_play['y'])
            print(f"This is other_playes {other_playes}")
            if other_playes and unique_id != other_players[0][0]['id']:
                spikebottom.update_pos(screen, other_players[-1][2]['spikebottomx'], other_players[-1][2]['spikebottomy'])
                #print(f"This is spiketop coordinates {other_players[0][1]['spiketopx']},{other_players[0][1]['spiketopy']} ")
                spiketop.update_pos(screen, other_players[-1][1]['spiketopx'], other_players[-1][1]['spiketopy'])

            elif other_players and unique_id == other_players[0][0]['id']:
                #other_players.remove(other_players[0])
                print(f"This is working")
                spiketop.move()
                spikebottom.move()
                spikebottom.draw(screen)
                spiketop.draw(screen, spikebottom)
            else:
                spiketop.move()
                spikebottom.move()
                spikebottom.draw(screen)
                spiketop.draw(screen, spikebottom)
            #spike.move()
            #spike.draw(screen)
            player.move()
            player.draw(screen)
            
            #enemy.draw(screen)
                    
        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)
    # Close the connection
    client.close()
    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
