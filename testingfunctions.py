from birdgame import Bird
import random
import pygame
other_player = {'id': 1, 'x':200, 'y':200}
other_player['bird'] = Bird(200,200)

clients = [1,2,4]
#print(clients[0])
clients.remove(clients[0])
#print(clients[0])

other_players = [{'game_done': True}, {'game_done': False}, {'game_done': True}]
result = all(player['game_done'] == True for player in other_players)
#print(result)


other_players = {'801890': True, '940-194-91': True, '28371111': True}


game_over = all(i for i in list(other_players.values()))
print(game_over)

current_time = pygame.time.get_ticks()
def delay(current_time, time_of_delay):
    end_time = 0
    while (end_time - current_time) <= time_of_delay:
        end_time = pygame.time.get_ticks()
    return True