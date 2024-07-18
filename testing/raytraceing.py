import sys, pygame

pygame.init()

screen = pygame.display.set_mode((600, 600))

clock = pygame.time.Clock()

x, y = 300, 300

prect = pygame.Rect(x, y, 50, 50)

testrect = pygame.Rect( 100, 100, 50, 50)

testcolor = (255, 0, 0)

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        y -= 5
    if keys[pygame.K_DOWN]:
        y += 5
    if keys[pygame.K_LEFT]:
        x -= 5
    if keys[pygame.K_RIGHT]:
        x += 5

    prect.topleft = (x, y)

    if prect.colliderect(testrect):
        if prect.y < testrect.y:
            y -= 5
        elif prect.y > testrect.y:
            y += 5

        if prect.x < testrect.x:
            x -= 5
        elif prect.x > testrect.x:
            x += 5

    prect.topleft = (x, y)

    pygame.draw.rect(screen, testcolor, testrect)
    pygame.draw.rect(screen, (255, 255, 255), prect)
    pygame.display.flip()

    clock.tick(60)