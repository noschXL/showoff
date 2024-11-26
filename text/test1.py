resolution = 100

import sys
import pygame
import bezier


pygame.init()

screen = pygame.display.set_mode((1000,1000))

dots = [bezier.Vector(100,500), bezier.Vector(500,500), bezier.Vector(900,500)]

bezier.DrawBezier(screen, dots[0], dots[1], dots[2], 100)

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pressed = pygame.mouse.get_pressed()[0]

    if pressed:
        dots[1] = bezier.Vector(*pygame.mouse.get_pos())

    lines = bezier.DrawBezier(screen, dots[0], dots[1], dots[2], resolution)
    for line in lines:
        pygame.draw.line(screen, "#00FFFF", line[0].xy(), line[1].xy(), 5)

    for dot in dots:
        pygame.draw.circle(screen, (255,255,255),(dot.x, dot.y), 10)
        
    pygame.display.flip()