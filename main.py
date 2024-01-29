import pygame
from player import *

pygame.init()

display = pygame.display.set_mode((1200, 950))

clock = pygame.time.Clock()

tiles = []
def updateTiles(scroll_x):
    with open("level") as f:
        lines = f.readlines()
        tiles.clear()

        for y, row in enumerate(lines):
            for x, item in enumerate(row):

                item = item.strip().lower()
                if item == "x":
                    tiles.append(pygame.Rect(x * 80 - scroll_x, y * 80, 80, 80))
            

player = Player(pygame.Vector2(50, 50), display)

running = True
while running:
    display.fill((100, 100, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    updateTiles(player.scroll_x)
    for tile in tiles:
        pygame.draw.rect(display, (255, 50, 50), tile)

    player.update(tiles)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
