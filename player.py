import pygame
import time
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.DOWN_KEY, self.UP_KEY, self.FACING_LEFT = False, False, False, False, False
        self.is_jumping, self.on_ground, self.digging = False, False, False
        self.gravity, self.friction = .35, -.12
        self.idle_1 = Spritesheet('Player.png').parse_sprite('playerIdle1.png')
        self.idle_2 = Spritesheet('Player.png').parse_sprite('playerIdle2.png')
        self.idle_3 = Spritesheet('Player.png').parse_sprite('playerIdle3.png')
        self.rect = self.idle_1.get_rect()
        self.position, self.velocity = pygame.math.Vector2(0,0), pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,self.gravity)
        self.walking_l1 = Spritesheet('Player.png').parse_sprite('playerWalk1.png')
        self.walking_l2 = Spritesheet('Player.png').parse_sprite('playerWalk2.png')
        self.time_1 = time.time()
        self.time_2 = time.time()
        self.life = 3
        self.gems = 0
        self.money = 0

    def draw(self, display):
        if self.on_ground == False:
            display.blit(self.idle_2, (self.rect.x, self.rect.y))
        elif self.LEFT_KEY == True:
            if time.time() - self.time_2 < 0.333:
                display.blit(self.walking_l1, (self.rect.x, self.rect.y))
            if time.time() -self.time_2 > 0.333:
                display.blit(self.walking_l2, (self.rect.x, self.rect.y))
            if time.time() -self.time_2 > 0.666:
                self.time_2 = time.time()
        elif self.RIGHT_KEY == True:
            if time.time() - self.time_2 < 0.333:
                display.blit(self.walking_l1, (self.rect.x, self.rect.y))
            if time.time() - self.time_2 > 0.333:
                display.blit(self.walking_l2, (self.rect.x, self.rect.y))
            if time.time() - self.time_2 > 0.666:
                self.time_2 = time.time()
        else:
            if time.time() - self.time_1 < 0.666:
                display.blit(self.idle_1, (self.rect.x, self.rect.y))
            elif time.time() - self.time_1 > 0.666 and time.time() - self.time_1 < 0.999:
                display.blit(self.idle_2, (self.rect.x, self.rect.y))
            elif time.time() - self.time_1 > 0.999:
                display.blit(self.idle_3, (self.rect.x, self.rect.y))
                if time.time() - self.time_1 > 1.333:
                    self.time_1 = time.time()


    def update(self, dt, tiles):
        self.horizontal_movement(dt)
        removeCollisions = self.checkCollisionsx(tiles)
        self.vertical_movement(dt)
        removeCollisions = removeCollisions + self.checkCollisionsy(tiles)
        numR = 0
        for i in range(0, len(removeCollisions)):
            i -= numR
            if tiles[removeCollisions[i]].tiletype == 6:
                removeCollisions.pop(i)
                numR += 1
            elif tiles[removeCollisions[i]].tiletype == 7:
                self.gems += 1
                print(self.gems)
                #numR += 1
        return(removeCollisions)

    def horizontal_movement(self,dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= .3
        elif self.RIGHT_KEY:
            self.acceleration.x += .3
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.rect.x = self.position.x

    def vertical_movement(self,dt):
#        print("vert: ", self.acceleration.y, self.velocity.y)
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.bottom = self.position.y
        if self.gems > 0:
            if self.position.x > -16.0 and self.position.x < 16 and self.position.y < 17:
                self.money += self.gems * 10
                self.gems = 0
                print("you have sold your gems")
                print("you now have", self.money, "$")


    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 8
            self.on_ground = False

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if tile.tiletype == 1 or tile.tiletype == 2 or tile.tiletype == 6 or tile.tiletype == 7:
                if self.rect.colliderect(tile):
                    hits.append(tile)
        return hits

    def get_hit_index(self, tiles):
        hits = []
        i = 0
        for j in range(0, len(tiles)):
            tile = tiles[i]
            if tile.tiletype == 1 or tile.tiletype == 2 or tile.tiletype == 6 or tile.tiletype == 7:
                if self.rect.colliderect(tile):
                    hits.append(i)
            if tile.tiletype == 6:
                if tiles[j-1].tiletype == 4:
                    tiles[j-1].tiletype = 6

            i += 1
        return hits

#    def checkCollisionsx(self, tiles):
#        collisions = self.get_hits(tiles)
#
#        for tile in collisions:
#            if self.velocity.x > 0:  # Hit tile moving right
#                self.position.x = tile.rect.left - self.rect.w
#                self.rect.x = self.position.x
#            elif self.velocity.x < 0:  # Hit tile moving left
#                self.position.x = tile.rect.right
#                self.rect.x = self.position.x

    def checkCollisionsx(self, tiles):
        collisions = self.get_hit_index(tiles)
        fastcollisions = []
        facingWall = False
        for i in collisions:
            if self.velocity.x > 0:  # Hit tile moving right
                self.position.x = tiles[i].rect.left - self.rect.w
                self.rect.x = self.position.x
                if self.RIGHT_KEY:
                    facingWall = True
            elif self.velocity.x < 0:  # Hit tile moving left
                self.position.x = tiles[i].rect.right
                self.rect.x = self.position.x
                if self.LEFT_KEY:
                    facingWall = True
            if self.digging == True and facingWall:
                fastcollisions.append(i)
            self.velocity.x = 0
        return fastcollisions



    def checkCollisionsy(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hit_index(tiles)
        fastcollisions = []
        facingWall=False
        for i in collisions:
            if self.velocity.y > 0:  # Hit tile from the top
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tiles[i].rect.top
                self.rect.bottom = self.position.y
                if self.DOWN_KEY:
                    facingWall = True
            elif self.velocity.y < 0:  # Hit tile from the bottom
                self.velocity.y = 0
                self.position.y = tiles[i].rect.bottom + self.rect.h
                self.rect.bottom = self.position.y
                if self.UP_KEY:
                    facingWall = True
#            if keyboard.is_pressed("w") and digging == 1:
            if self.digging and facingWall:
                fastcollisions.append(i)
        return fastcollisions






