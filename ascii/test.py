import pygame, decoder, sys

width, height, data = decoder.decodepng("/home/nosch/Documents/logo2.png")

pygame.init()

screen = pygame.display.set_mode((width, height))
screen.fill("#000000")


for x in range(width):
    for y in range(width):
        newsurf = pygame.Surface((1,1))
        pygame.draw.rect(newsurf, pygame.Color(data[x][y][0], data[x][y][1], data[x][y][2]), (0,0,1,1))
        newsurf.set_alpha(data[x][y][3])
        screen.blit(newsurf, (x,y))

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit