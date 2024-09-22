import pygame

from sys import exit

#STATES:
SLEEPING = 0
WORKING = 1
UPGRADING = 2
BUYING = 3

state = 0

while True:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            exit()
