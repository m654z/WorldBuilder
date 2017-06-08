import pygame
import random
import sys
import json
from pygame.locals import *

class Tilemap:
    tilemap = [[0]*40]*40 # The actual tilemap

    def __init__(self, textures, tilesize, width, height, borders=0):
        self.textures = textures # List of textures in dictionary format
        self.tilesize = tilesize + borders # The size of a tile
        self.width = width # How many tiles wide the map is
        self.height = height # How many tile high the map is
        self.borders = borders
        self.window_size = [self.tilesize*self.width-borders,
                            self.tilesize*self.height-borders]
        self.mapsize = [self.width, self.height]
        self.bottom_row = self.height-1
        self.side_row = self.width-1
        self.selected = [0, 0]
        self.selected_texture = None

    def generate_random(self, exclude=[], seed=random.seed()):
        """Generate a random tilemap"""
        allowed = list(range(len(self.textures)))
        try:
            for texture in exclude:
                allowed.remove(texture)
        except TypeError:
            print("""ERROR: generate_random() takes a list as an argument.
Instead it found a"""+str(type(exclude))+"""
For example, tilemap.generate_random(exclude=[0,3,4])
Currently running generate_random() with no arguments."""+"\n")
            sys.exit()
        self.tilemap = [[random.choice(allowed) for e in range(
        self.width)] for e in range(self.height)]

    def generate(self, number, life, tile):
        """Generate 'blobs' of textures using 'ants'"""
        ants = []
        for i in range(number):
            ants.append(Ant([random.randint(0, self.width-1),
             random.randint(0, self.height-1)], life, self.mapsize,
             self, tile))

        for ant in ants:
            while ant.life > 1:
                ant.move()
                try:
                    self.tilemap[ant.position[0]][ant.position[1]] = ant.tile
                except IndexError:
                    ant.position[0] += 1
                    ant.position[1] += 1
            ants.remove(ant)

    def fill(self, texture):
        """Fill the entire tilemap with a certain texture"""
        self.tilemap = [[texture for e in range(self.width)] for e in range(
        self.height)]

    def fill_row(self, texture, row, freq=0, skip=[], pos=[0, None]):
        """Place a texture in a row"""
        if pos[1] == None:
            pos[1] = self.width
        for i in range(pos[0], pos[1]):
            if random.randint(0, freq) == freq:
                if self.tilemap[row][i] in skip:
                    pass
                else:
                    self.tilemap[row][i] = texture

    def fill_col(self, texture, col, freq=0, skip=[], pos=[0, None]):
        """Place a texture in a column"""
        if pos[1] == None:
            pos[1] = self.width
        for i in range(pos[0], pos[1]):
            if random.randint(0, freq) == freq:
                if self.tilemap[i][col] in skip:
                    pass
                else:
                    self.tilemap[i][col] = texture

    def replace(self, textures, replacement):
        """Replace every instance of a texture with another one"""
        for row in range(self.height):
            for column in range(self.width):
                if self.tilemap[row][column] in textures:
                    self.tilemap[row][column] = replacement

    def remove_single(self, tiles, replacement):
        """Remove single tiles"""
        for tile in tiles:
            for row in range(self.height):
                for column in range(self.width):
                    if self.tilemap[row][column] == tile:
                        if not self.next_to([row, column], tile):
                            self.tilemap[row][column] = replacement

    def next_to(self, position, tile):
        """Check if a tile is next to another one"""
        try:
            if self.tilemap[position[0]][position[1]+1] == tile:
                return True
        except IndexError: pass
        try:
            if self.tilemap[position[0]][position[1]-1] == tile:
                return True
        except IndexError: pass
        try:
            if self.tilemap[position[0]+1][position[1]] == tile:
                return True
        except IndexError: pass
        try:
            if self.tilemap[position[0]-1][position[1]] == tile:
                return True
        except IndexError: pass
        return False
    
    def get_tile(self, position, tiles):
        """Check if a tilemap position contains a certain tile"""
        if self.tilemap[position[0]][position[1]] in tiles:
            return True
        else:
            return False

    def json_dump(self, file_name):
        """Save the tilemap as a JSON file"""
        with open(file_name, 'w') as f:
            dumped = json.dumps(self.tilemap)
            f.write(dumped)

    def json_load(self, file_name):
        """Load a JSON file"""
        with open(file_name, 'r') as f:
            self.tilemap = json.loads(f.read())

    def on_screen(self, pos):
        """Check if a tile is on the screen"""
        return not (pos[0] < self.tilesize or pos[0] > self.width*self.tilesize
                    or pos[1] < self.tilesize or pos[1] > self.height*self.tilesize)

    def draw(self, display):
        """Draw the tilemap"""
        try:
            for row in range(self.height):
                for column in range(self.width):
                    display.blit(self.textures[self.tilemap[row][column]],
                                        (column*self.tilesize,
                                        row*self.tilesize))
                    #display.blit(self.textures[self.tilemap[row][column]],
                    #self.camera.apply(pygame.rect.Rect((column*self.tilesize,
                                                       # row*self.tilesize),
                                                #(self.tilesize,
                                                #self.tilesize))))
        except KeyError:
            print("""ERROR: the draw() function is trying to load
a texture that doesn't exist. Are you sure it's in the dictionary?\n
"""+str(self.textures) + "\n")
            sys.exit()
        except TypeError:
            print("""ERROR: the draw() function is trying to draw
something that isn't a pygame.Surface object.\n\n"""+
str(self.textures) + "\n")
            sys.exit()
        except IndexError:
            print("""ERROR: the tilemap seems to be empty.\n\n"""+
str(self.tilemap) + "\n")
            sys.exit()

class Unit:
    def __init__(self, image, tilemap, position=[0,0]):
        self.image = image
        self.tilemap = tilemap
        self.position = position

    def draw(self, display):
        """Draw the unit"""
        display.blit(self.image,[self.position[0]*self.tilemap.tilesize,
        self.position[1]*self.tilemap.tilesize])

    def move_up(self, block=[], wrap=False):
        """Move the unit up"""
        if self.position[1] > 0:
            if not self.tilemap.tilemap[self.position[1]-1][self.position[0]] in block:
                self.position[1] -= 1
        if wrap == True:
            if self.position[1] == 0:
                self.position[1] = self.tilemap.bottom_row

    def move_down(self, block=[], wrap=False):
        """Move the unit down"""
        if self.position[1] < self.tilemap.height - 1:
            if not self.tilemap.tilemap[self.position[1]+1][self.position[0]] in block:
                self.position[1] += 1
        if wrap == True:
            if self.position[1] == self.tilemap.bottom_row:
                self.position[1] = 0

    def move_right(self, block=[], wrap=False):
        """Move the unit right"""
        if self.position[0] < self.tilemap.width - 1:
            if not self.tilemap.tilemap[self.position[1]][self.position[0]+1] in block:
                self.position[0] += 1
        if wrap == True:
            if self.position[0] == self.tilemap.side_row:
                self.position[0] = 0

    def move_left(self, block=[], wrap=False):
        """Move the unit left"""
        if self.position[0] > 0:
            if not self.tilemap.tilemap[self.position[1]][self.position[0]-1] in block:
                self.position[0] -= 1
        if wrap == True:
            if self.position[0] == 0:
                self.position[0] = self.tilemap.side_row

class Scripts:
    """A collection of useful generation scripts."""
    def __init__(self, tilemap):
        self.tilemap = tilemap

    def islands(self, tile1, tile2, amount, size):
        """Creates random blobs of tile2 inside a map full of tile2."""
        self.tilemap.fill(tile1)
        self.tilemap.generate(amount, size, tile2)
        self.tilemap.remove_single([tile2], tile1)

    def lakes(self, tile1, amount, size, tile2=False):
        """Creates random blobs of tile2, optionally replacing singular tiles with tile2."""
        self.tilemap.generate(amount, size, tile1)
        if tile2 != False:
            self.tilemap.remove_single([tile1], tile2)

    def fade(self, tile1):
        """Creates a 'fade' effect at the top and bottom rows."""
        self.tilemap.fill_row(tile1, 0)
        self.tilemap.fill_row(tile1, 1, 1)
        self.tilemap.fill_row(tile1, tilemap.bottom_row)
        self.tilemap.fill_row(tile1, tilemap.bottom_row-1, 1)
                
class Ant:
    # Ant idea from http://stackoverflow.com/a/4800633/5198106... Thank you!
    """Moves around randomly, creating 'realistic' blobs of textures"""
    def __init__(self, position, life, mapsize, tilemap, tile):
        self.position = position
        self.life = life
        self.mapsize = mapsize
        self.tilemap = tilemap
        self.tile = tile

    def move(self):
        """Move in a random direction"""
        direction = random.randint(0, 3)
        if direction == 0: self.position[0] += 1
        elif direction == 1: self.position[0] -= 1
        elif direction == 2: self.position[1] += 1
        elif direction == 3: self.position[1] -= 1
        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[0] > self.mapsize[0]:
            self.position[0] = self.mapsize[0]
        if self.position[1] < 0:
            self.position[1] = 1
        if self.position[1] > self.mapsize[1]:
            self.position[1] = self.mapsize[1]
        self.life -= 1
        try:
            if not self.tilemap.next_to(self.position, self.tile):
                self.move()
        except:
            if self.tile not in self.tilemap.textures:
                print("""ERROR: An ant is trying to draw a texture
that doesn't exist: """ + str(self.tile) + "\n")
                sys.exit()
            else:
                print("""ERROR: Something went wrong with an ant.
It's position was """ + str(self.position) + " and it was drawing texture " +
str(self.tile) + "\n")
                sys.exit()
