#WorldBuilder

WorldBuilder is a simple application written in Python and Pygame that makes it easy to create tilemaps for games.
WorldBuilder uses the PyTilemap library, and exports finished tilemaps with the JSON file format, making it easy to use with PyTilemap.

When you open WorldBuilder you'll be asked how many tiles you want to use. The maximum is currently 9. Next, you'll be asked for the filenames.
After you've inputted all of the filenames, input the size of the tiles. For example, if the tiles are 32x32, input 32.
Next, input the size of the map. If you want it to be 20x20, input 20 20.
Finally, input the size of the border in between the tiles in pixels.

##Controls

0 - select blank tile
123456789 - select tiles
(space) - place tile
R - fill row
C - fill column
F - fill map
F1 - randomize tilemap

##Navigational Controls

Arrow keys - move around
HOME - move to beginning of row
END - move to end of row
PAGE UP - move to top of column
PAGE DOWN - move to bottom of column

##Saving and Loading

S - Save tilemap
L - Load tilemap