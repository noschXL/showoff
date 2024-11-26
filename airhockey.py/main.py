import high_math
import pygame
import sys
import os

pygame.init()

width, height = 1000, 1500

screen = pygame.display.set_mode((width, height))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()