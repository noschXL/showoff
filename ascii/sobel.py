import pygame
import sys
import time
import numpy as np

pygame.init()

def greyscale(surface: pygame.Surface):
    arr = pygame.surfarray.array3d(surface)
    # calulates the avg of the "rgb" values, this reduces the dim by 1
    mean_arr = np.mean(arr, axis=2)
    # restores the dimension from 2 to 3
    mean_arr3d = mean_arr[..., np.newaxis]
    # repeat the avg value obtained before over the axis 2
    new_arr = np.repeat(mean_arr3d[:, :, :], 3, axis=2)
    # return the new surface
    return pygame.surfarray.make_surface(new_arr)


def sobel(path: str, n: int): #path to image, image scale
    try:
        img = pygame.image.load(path)
    except:
        print(f"couldnt load the image at {path}")
        sys.exit()

    img = pygame.transform.scale_by(img, n)
    img = pygame.transform.scale_by(img, 1 / 8)

            
    imgmap = [[] for _ in range(img.get_width())]
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color = img.get_at((x,y)).b
            color = (round(color / (255 / 2)) - 1) * 255
            imgmap[x].append(color)


    imgmap = [[] for _ in range(img.get_width())]
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color = img.get_at((x,y)).b
            color = (round(color / (255 / 2)) - 1) * 255
            imgmap[x].append(color)

    picture = ["0" * img.get_width() * 2 for _ in range(img.get_height())]



    for x in range(img.get_height()):
        for y in range(img.get_height()):
            Gx, Gy = 0,0
            try:
                Gx = (imgmap[x-1][y + 1] + 2 * imgmap[x-1][y] + imgmap[x-1][y - 1]) - (imgmap[x+1][y + 1] + 2 * imgmap[x+1][y] + imgmap[x+1][y - 1])
            except IndexError:
                pass
            try:
                Gy = (imgmap[x-1][y - 1] + 2 * imgmap[x][y - 1] + imgmap[x + 1][y - 1]) - (imgmap[x-1][y + 1] + 2 * imgmap[x-1][y] + imgmap[x-1][y - 1])
            except IndexError:
                pass

            char = "0"

            if abs(Gx) < 500:
                Gx = 0
            if abs(Gy) < 500:
                Gy = 0

            if Gx != 0:
                Gx = Gx / abs(Gx)
            if Gy != 0:
                Gy = Gy / abs(Gy)
            direction = [Gx, Gy]
            if direction != [0,0]:
                '''
                if direction == [1,-1] or direction == [-1,0]:
                    char = "|"
                elif direction == [0,1] or direction == [0,-1]:
                    char = "-"
                elif direction == [-1,1] or direction == [1,0]:
                    char = chr(92)
                elif direction == [-1,-1] or direction == [1,1]:
                    char = "/"
                '''

                if direction == [0,1]:
                    char = "~"
                elif direction == [1,0]:
                    char = "/"
                elif direction == [0,-1]:
                    char = "~"
                elif direction == [-1,0]:
                    char = "/"
                elif direction == [1,1]:
                    char = "~"
                elif direction == [1,-1]:
                    char = chr(92)
                elif direction == [-1,-1]:
                    char = "~"
                elif direction == [-1,1]:
                    char = chr(92)
            if char != "0":
                row = list(picture[y])
                row[x * 2] = char
                row[x * 2 + 1] = char
                picture[y] = "".join(row)


            #if direction != [0,0]:
                #pygame.draw.circle(img, (255 * abs(direction[0]), 255 * abs(direction[1]), 0), (x,y), 1)

    return picture

def getoutline(path, n):
    picture = sobel(path, n / 2)
    return picture

if __name__ == "__main__":
    start = time.time()
    picture = sobel("/home/nosch/Documents/mint.png", 1.5)
    print(time.time()- start)
    #screen = pygame.display.set_mode((img.get_width(), img.get_height()))
    #screen.blit(img, (0,0))
    #pygame.display.flip()
    for row in picture:
        print(row)
