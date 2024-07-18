import pygame
import sys
import math
import sobel

if len(sys.argv) == 1:
    print("this was originally made by noschXL")
    print("Usage: python asciiart.py -p [path] -c -s [size]")
    print("-p [path]    set the image path")
    print("-c           activate colormode")
    print("-s [size]    set the multiplication size, 1 by default")
    print("-h           show this help message")
    sys.exit()

path = None
colorized = False
n = 1
args = sys.argv[1:]
for p, arg in enumerate(args):
    print(arg)
    if arg[0] == "-":
        if arg == "-h":
            print("this was originally made by noschXL")
            print("Usage: python asciiart.py -p [path] -c -s [size]")
            print("-p [path]    set the image path")
            print("-c           activate colormode")
            print("-s [size]    set the multiplication size, 1 by default")
            print("-h           show this help message")
            sys.exit()
        if arg == "-c":
            colorized = True
        elif arg[0:2] == "-s":
            print(p)
            n = int(args[p+1])
        elif arg[0:2] == "-p":
            path = args[p+1]

if path is None:
    print("please specify a image path using -[path]")
    sys.exit()

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
outline = sobel.getoutline(path, n)

#generating ascii
picture = []
for y in range(math.ceil(imgrect.height / 2)):
    row = ""

    for x in range(imgrect.width):
        pixel = img.get_at((x,y * 2))
        brightness = pixel.grayscale()
        
        char = chars[round(brightness.g / (255 / len(chars))) - 1]
        row += char
    picture.append(row)

picture: list[str] = picture

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
    