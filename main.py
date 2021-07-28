import pygame as pygame

from tiles import *
import time
from spritesheet import Spritesheet
from player import Player
################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
pygame.init()
DISPLAY_W, DISPLAY_H = 960, 540
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
clock = pygame.time.Clock()
TARGET_FPS = 60
################################# LOAD PLAYER AND SPRITESHEET###################################
spritesheet = Spritesheet('spritesheet.png')
player = Player()
#################################### LOAD THE LEVEL #######################################
map = TileMap('test_level.csv', spritesheet )
player.position.x, player.position.y = 0, -10
dt = clock.tick(60)

################################# GAME LOOP ##########################
while running:
#    print(player.position.y)
#    print(player.velocity.y)
#    player.position.y = 10
#    print("dt")
    dt = clock.tick(60)
#    print(dt)
    dt = dt * .001 * TARGET_FPS
#    print(dt)
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.LEFT_KEY = True
            elif event.key == pygame.K_RIGHT:
                player.RIGHT_KEY = True
            elif event.key == pygame.K_UP:
                player.UP_KEY = True
            elif event.key == pygame.K_DOWN:
                player.DOWN_KEY = True
            elif event.key == pygame.K_SPACE:
                player.jump()
            elif event.key == pygame.K_w:
                player.digging = True


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.LEFT_KEY = False
            elif event.key == pygame.K_RIGHT:
                player.RIGHT_KEY = False
            elif event.key == pygame.K_UP:
                player.UP_KEY = False
            elif event.key == pygame.K_DOWN:
                player.DOWN_KEY = False
            elif event.key == pygame.K_SPACE:
                if player.is_jumping:
                    player.velocity.y *= .25
                    player.is_jumping = False
            elif event.key == pygame.K_w:
                player.digging = False


    ################################# UPDATE/ Animate SPRITE #################################
#    removedtiles = player.update(dt, map.tiles)
    #time.sleep(1.0)
    removedtiles = player.update(dt, map.tiles)
    map.removeTiles(removedtiles)
    ################################# UPDATE WINDOW AND DISPLAY #################################
    canvas.fill((0, 180, 240)) # Fills the entire screen with light blue
    map.draw_map(canvas)
    player.draw(canvas)
    window.blit(canvas, (0,0))
#    window.blit(map.map_surface, (0,0))
    pygame.display.update()









