import pygame, csv, os, random
tiles = 0

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet, tiletype):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.tiletype = tiletype

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Blob():
    def __init__(self, x, y, strength, R):
        self.x, self.y, self.strength, self.R = x, y, strength, R
        self.R2 = self.R ** 2
    def field(self, x, y):
        if abs(y-self.y) > self.R or abs(x-self.x) > self.R:
            return 0
        d2 = (y - self.y) ** 2 + (x - self.x) ** 2
        if d2 > self.R2:
            return 0
        else:
            return self.strength * (1 - 0.444444 * ((d2 ** 4) / (self.R2 ** 4)) + 1.888889 * ((d2 ** 2) / (self.R2 ** 2)) - 2.444444 * (d2 / self.R2))

class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.blobs = []
        self.spritesheet = spritesheet
#        self.tiles = self.load_tiles(filename)
#        self.tiles = self.random_tiles(30, 17)
        self.cols = 60
        self.rows = 34
        self.map_matrix = [0] * (self.rows*self.cols)
        self.tiles = self.randblob_tiles(self.cols, self.rows, 180)

        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()
#        for i in self.map_matrix:
#            print(i)

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
#        R = 7
        for i in range(0,numblobs):
            self.blobs.append(Blob(random.randint(-20,width+20), random.randint(-20,height+20), random.random()*2, random.randint(3,11)))
        for i in range(0,numblobs):
            self.blobs.append(Blob(random.randint(-20, width + 20), random.randint(-20, height + 20), random.random()*-2, random.randint(3,11)))
        tiles = []
        x, y = 0, 0
        for row in range(0, height):
            x = 0
            # Move to next tile in current row
            for col in range(0, width):
                field = 0
                for blob in self.blobs:
                    field = field + blob.field(x,y)

                ran = 2

                if x == width - 1:
                    ran = 2
                if x == 0:
                    ran = 2
                if y == height - 1:
                    ran = 1

                if field > 0:
#                if field > 0.5:
                    ran = 2
                elif field > -0.6:
#                if field > 0.95:
                    ran = 1
                elif field > -1.2:
                    ran = 3
                else:
                    ran = 4
                if x == 0   and y == 0:
                    ran = 0
                if (x == 0 or x == 1) and y == 1:
                    ran = 2
                #                if ran == range(0, 5):
                #                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                if ran == 1:
                    tiles.append(Tile('grass.png', x * self.tile_size, y * self.tile_size, self.spritesheet, 1))
                if ran == 2:
                    rando = random.random()
                    if rando > 0.9:
                        ran = 6
                        tiles.append(Tile('lava.png', x * self.tile_size, y * self.tile_size, self.spritesheet, 6))
                    elif rando > 0.8 and rando < 0.9:
                        ran = 7
                        tiles.append(Tile('grass.png', x * self.tile_size, y * self.tile_size, self.spritesheet, 7))
                    else:
                        tiles.append(Tile('grass2.png', x * self.tile_size, y * self.tile_size, self.spritesheet, 2))
                if ran == 3:
                    tiles.append(Tile('cave1.png', x * self.tile_size, y * self.tile_size, self.spritesheet, 3))
                if ran == 4:
                    tiles.append(Tile('cave2.png', x * self.tile_size, y * self.tile_size, self.spritesheet, 4))
                self.map_matrix[y*self.cols+x] = ran
#                print("xy", y, x, y*self.cols+x)
#                print(ran)
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
            y = int(i / self.cols)
            x = i % self.cols+1
            self.tiles[i] = Tile('cave1.png', x * self.tile_size, y * self.tile_size, self.spritesheet, 3)
#            self.tiles.pop(i-numCollisions)
            numCollisions += 1
        if numCollisions > 0:
            self.load_map()

