import sys
import math
import sobel

if len(sys.argv) == 1:
    print("This was originally made by noschXL.\n")
    print("It uses the pygame library to load the images.")
    print("To install pygame: pip install pygame.\n")
    print("Usage: python asciiart.py -p [path]")
    print("-p [path]    set the image path")
    print(f"-c           \033[38;2;255;0;0mcolormode\033[0m")
    print("-s [size]    set the multiplication size, 1 by default")
    print("-o           draw outline (experimental)")
    print("-h           show this help message")
    sys.exit()

path = None
colorized = False
outlineb = False
n = 1
args = sys.argv[1:]
for p, arg in enumerate(args):
    print(arg)
    if arg[0] == "-":
        if arg == "-h":
            print("This was originally made by noschXL.\n")
            print("It uses the pygame library to load the images.")
            print("To install pygame: pip install pygame.\n")
            print("Usage: python asciiart.py -p [path] -c -s [size]")
            print("-p [path]    set the image path")
            print(f"-c           \033[38;2;255;0;0mcolormode\033[0m")
            print("-s [size]    set the multiplication size, 1 by default")
            print("-o           draw outline (experimental)")
            print("-h           show this help message")
            sys.exit()
        if arg == "-c":
            colorized = True
        elif arg == "-o":
            outlineb = True
        elif arg[0:2] == "-s":
            n = float(args[p+1])
        elif arg[0:2] == "-p":
            path = args[p+1]

if path is None:
    print("please specify a image path using -[path]")
    sys.exit()

import pygame
pygame.init()

chars = '.,*+#@'

try:
    img = pygame.image.load(path)
except:
    print(f"couldnt load the image at {path}")
    sys.exit()

img = pygame.transform.scale_by(img, n)
img = pygame.transform.scale_by(img, 1 / 8)

imgrect = img.get_rect()

#generating outline
if not outlineb:
    outline = sobel.getoutline(path, n)

#generating ascii
picture = []
for y in range(math.ceil(imgrect.height / 2)):
    row = ""

    for x in range(imgrect.width):
        pixel = img.get_at((x,y * 2))
        brightness = pixel.grayscale()
        
        char = chars[round(brightness.g / (255 / len(chars))) - 1]
        if colorized and outlineb:
            row += f"\033[38;2;{pixel.r};{pixel.g};{pixel.b}m{char}\033[0m"
        else:
            row += char
    picture.append(row)

picture: list[str] = picture

if outlineb:
    for row in picture:
        print(row)
    sys.exit()

# generating ascii with outline
newpicture = []
for y in range(len(picture) - 1):
    row = ""
    for x in range(len(picture[y]) - 1):
        char = picture[y][x]
        outchar = outline[y][x]
        if outchar == "0":
            row += char
        else:
            row += outchar
    newpicture.append(row)

charlist = []

for row in newpicture:
    charlist.append(list(row))

finalpicture = []


# coloring ascii
for y in range(len(charlist)):
    row = ""
    for x in range(len(charlist[y])):
        char = charlist[y][x]
        if colorized:
            color = img.get_at((x, math.ceil(y * 2))) 
            row += f"\033[38;2;{color.r};{color.g};{color.b}m{char}\033[0m"
        else:
            row += char
    finalpicture.append(row)


for row in finalpicture:
    print(row)
    