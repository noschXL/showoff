import pygame
import high_math

class Puck:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface(self.rect)
        self.speed = 200
        self.direction = high_math.Vector(0,0)

    def update(self, dt, walls: list):    
        self.rect.x += high_math.math.cos(self.direction.x) * self.speed * dt
        self.rect.y += high_math.math.sin(self.direction.y) * self.speed * dt

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                oldposx = self.rect.x - self.direction.x * self.speed * dt
                oldposy = self.rect.y - self.direction.y * self.speed * dt

                #get the side of the collison

                if oldposx < wall.rect.x:
                    tangent = high_math.Vector(-self.direction.y, self.direction.x)
                elif oldposx > wall.rect.right:
                    tangent = high_math.Vector(-self.direction.y, self.direction.x)
class Wall:
    def __init__(self, x, y, width, height, movex = 0):
        self.rect = pygame.Rect(x, y, width, height)
        self.movex = movex
        self.moving = x == movex
        self.surface = pygame.Surface(self.rect)
        self.movleft = False

    def update(self, dt, puck):
        if self.moving:
            self.rect.x += self.movex if self.movleft else -self.movex
        
