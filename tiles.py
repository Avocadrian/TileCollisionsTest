import pygame, csv, os, random, keyboard, math
tiles = 0

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
#        self.tiles = self.load_tiles(filename)
#        self.tiles = self.random_tiles(30, 17)
        self.tiles = self.randblob_tiles(60, 34, 180)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0,0))

    def load_map(self):
        self.map_surface.fill((0,0,0))
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '1':
                    tiles.append(Tile('grass.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '2':
                    tiles.append(Tile('grass2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    # Move to next tile in current row

                    # Move to next tile in current row

                    x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles

    def random_tiles(self, width, height):
        tiles = []
        x, y = 0, 0
        for row in range(0,height):
            x = 0
                    # Move to next tile in current row
            for tile in range(0,width):
                ran = random.randint(0, 5)
                if x == width-1:
                    ran = 2
                if x == 0:
                    ran = 2
                if y == height-1:
                    ran = 1

#                if ran == range(0, 5):
#                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                if ran == 1:
                    tiles.append(Tile('grass.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                if ran == 2:
                    tiles.append(Tile('grass2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))

                # Move to next tile in current row

                x += 1

            # Move to next row
            y += 1

            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles

    def randblob_tiles(self, width, height, numblobs):
        blobs = []
        negBlobs = []
        R = 7
        for i in range(0,numblobs):
            blobs.append((random.randint(-20,width+20), random.randint(-20,height+20)))
        for i in range(0,numblobs):
            negBlobs.append((random.randint(-20,width+20), random.randint(-20,height+20)))
        tiles = []
        x, y = 0, 0
        for row in range(0, height):
            x = 0
            # Move to next tile in current row
            for col in range(0, width):
                field = 0;
                for blob in blobs:
                    dist = math.sqrt((y-blob[1])**2+(x-blob[0])**2)
                    if dist < R:
                        dist = 1-3*(dist/R)**2+3*(dist/R)**4-(dist/R)**6
                    else:
                        dist = 0
#                    print(dist)
#                    if(dist > 0):
#                        field = field + 1/dist
                    field = field + dist
#                    else:
#                        field = 1000000.0
#                    print(field)

                for blob in negBlobs:
                    dist = math.sqrt((y - blob[1]) ** 2 + (x - blob[0]) ** 2)
                    if dist < R:
                        dist = 1 - 3 * (dist / R) ** 2 + 3 * (dist / R) ** 4 - (dist / R) ** 6
                    else:
                        dist = 0
                    field = field - dist

                ran = 2

                if x == width - 1:
                    ran = 2
                if x == 0:
                    ran = 2
                if y == height - 1:
                    ran = 1

                if field > -0.6:
#                if field > 0.5:
                    ran = 1
                if field > 0:
#                if field > 0.95:
                    ran = 0
                if x == 0   and y == 0:
                    ran = 0
                if (x == 0 or x == 1) and y == 1:
                    ran = 2
                #                if ran == range(0, 5):
                #                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                if ran == 1:
                    tiles.append(Tile('grass.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                if ran == 2:
                    tiles.append(Tile('grass2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))

                # Move to next tile in current row

                x += 1

            # Move to next row
            y += 1

            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles

    def removeTiles(self, tileIndices):
        tileIndices.sort()
        numCollisions = 0
        for i in tileIndices:
            self.tiles.pop(i-numCollisions)
            numCollisions += 1
        if numCollisions > 0:
            self.load_map()

