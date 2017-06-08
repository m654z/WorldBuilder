import pygame
import sys
from tilemap import *
from pygame.locals import *

pygame.init()

images = {0: pygame.image.load("blank.png")}

tiles = int(input("How many tile image files? (max. 10) "))
for i in range(1, tiles+1):
    name = input("Image #" + str(i) + ": ")
    images[i] = pygame.image.load(name)
size = int(input("Size of tiles: "))
wh = input("Size of map: ").split(' ')
borders = int(input("Borders: "))

tilemap = Tilemap(images, size, int(wh[0]), int(wh[1]), borders)
tilemap.fill(0)
display = pygame.display.set_mode([tilemap.window_size[0],tilemap.window_size[1]+100])
select = Unit(pygame.image.load("selected.png"), tilemap)

texture = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                select.move_right()

            if event.key == K_LEFT:
                select.move_left()

            if event.key == K_UP:
                select.move_up()

            if event.key == K_DOWN:
                select.move_down()
            try:
                if event.key == K_SPACE:
                    tilemap.tilemap[select.position[1]][select.position[0]] = texture
                    select.position[0] += 1
                if event.key == K_0:
                    #tilemap.tilemap[select.position[1]][select.position[0]] = -1
                    texture = 0
                    #select.position[0] += 1
                if event.key == K_1:
                    #tilemap.tilemap[select.position[1]][select.position[0]] = 1
                    texture = 1
                    #select.position[0] += 1
                if event.key == K_2:
                    #tilemap.tilemap[select.position[1]][select.position[0]] = 2
                    texture = 2
                    #select.position[0] += 1
                if event.key == K_3:
                    #tilemap.tilemap[select.position[1]][select.position[0]] = 3
                    texture = 3
                    #select.position[0] += 1
                if event.key == K_4:
                    #tilemap.tilemap[select.position[1]][select.position[0]] = 4
                    texture = 4
                    #select.position[0] += 1
                if event.key == K_5:
                    #tilemap.tilemap[select.position[1]][select.position[0]] = 5
                    texture = 5
                    #select.position[0] += 1
                if event.key == K_6:
                    #tilemap.tilemap[select.position[1]][select.position[0]] = 6
                    texture = 6
                    #select.position[0] += 1
                if event.key == K_7:
                    #tilemap.tilemap[select.position[1]][select.position[0]] = 7
                    texture = 7
                    #select.position[0] += 1
                if event.key == K_8:
                    #tilemap.tilemap[select.position[1]][select.position[0]] = 8
                    texture = 8
                    #select.position[0] += 1
                if event.key == K_9:
                    #tilemap.tilemap[select.position[1]][select.position[0]] = 9
                    texture = 9
                    #select.position[0] += 1
            except:
                pass
            if event.key == K_r:
                tilemap.fill_row(texture, select.position[1])
            if event.key == K_c:
                tilemap.fill_col(texture, select.position[0])
            if event.key == K_f:
                tilemap.fill(texture)
            if event.key == K_F1:
                tilemap.generate_random([0])
            if event.key == K_BACKSPACE:
                tilemap.fill(0)
            if event.key == K_HOME:
                select.position[0] = 0
            if event.key == K_END:
                select.position[0] = tilemap.side_row
            if event.key == K_PAGEUP:
                select.position[1] = 0
            if event.key == K_PAGEDOWN:
                select.position[1] = tilemap.bottom_row
            if event.key == K_s:
                tilemap.json_dump(input("Save as: "))
            if event.key == K_l:
                try:
                    tilemap.json_load(input("Load from: "))
                except FileNotFoundError:
                    pass
    tilemap.draw(display)
    select.draw(display)
    try:
        display.blit(tilemap.textures[texture], (tilemap.window_size[0]-50, tilemap.window_size[1]+50))
    except:
        pass
    pygame.display.update()
        
