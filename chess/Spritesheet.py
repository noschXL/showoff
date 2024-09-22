import pygame


class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except FileNotFoundError as e:
            print(f'Unable to load spritesheet image: {filename} due to {e}')

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None, mult_size = 2):
        "Loads multiple images, supply a list of coordinates"
        imglist = []
        for rect in rects:
            image = self.image_at(rect, colorkey)
            image = pygame.transform.scale_by(image, mult_size)
            imglist.append(image)
        return imglist
