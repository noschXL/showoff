import pygame
import math

water_colors = [(255,255,255), (0,255,255), (0,200,200)]

def print2dList(list_to_print):
    for entity in list_to_print:
        print(entity)

class Water:
    class Surface:
        def __init__(self, screen, rect: pygame.Rect = None):
            if not isinstance(rect, pygame.Rect):
                raise TypeError("Please give a pygame.rect to Water.Surface")
            self.rects = rect
            self.map = [[[0,n]] * rect.width for n in range(rect.height)]
            print2dList(self.map)

        def update(self, wind_dir: int | None = None):
            pass

        def draw(self):
            pass


pygame.init()

screen = pygame.display.set_mode((600,600))
testsurf = Water.Surface(screen, pygame.Rect(0,0,16,16))

