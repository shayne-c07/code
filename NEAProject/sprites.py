# Sprite classes for game

import pygame
import random
from constants import *

from pygame.locals import (
    RLEACCEL,
    K_w,
    K_s,
    K_a,
    K_d,
    K_c,
    K_p,
    K_r,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

vec= pygame.math.Vector2

class slimePlayer(pygame.sprite.Sprite):
    def __init__(self, game):
        super(slimePlayer, self).__init__()
        self.game = game
        #ratio 3:4
        self.image = pygame.Surface((30,40))
        self.surf = pygame.image.load("slimeright.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.pos = vec(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)



    def jump(self):
        # self.rect.x+=1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        # self.rect.x -=1
        if hits:
            self.vel.y = -PLAYER_JUMP


    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_w]:
            global COOLDOWN
            if COOLDOWN <=0:
                pass
            else:
                self.acc.y = -PLAYER_ACC
                COOLDOWN -=0.5
                if self.vel.x <=0:
                    self.surf = pygame.image.load("jetpackleft.png").convert()
                    self.surf.set_colorkey((0, 0, 1), RLEACCEL)
                if self.vel.x >=0:
                    self.surf = pygame.image.load("jetpackright.png").convert()
                    self.surf.set_colorkey((0, 0, 1), RLEACCEL)

        if pressed_keys[K_s]:
            self.acc.y = PLAYER_ACC
        if pressed_keys[K_a]:
            self.acc.x = -PLAYER_ACC
            if self.vel.y >= 0:
                self.surf = pygame.image.load("slimeleft.png").convert()
                self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        if pressed_keys[K_d]:
            self.acc.x = PLAYER_ACC
            if self.vel.y >=0:
                self.surf = pygame.image.load("slimeright.png").convert()
                self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        if pygame.sprite.spritecollide(self, self.game.platforms, False):
            if COOLDOWN <=100:
                COOLDOWN += 1

        #motion + friction
        self.acc += self.vel * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        self.rect.midbottom= self.pos



        #barrier control validation algorithm
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x -= self.vel.x + 0.5 * self.acc.x
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.pos.x -= self.vel.x + 0.5 * self.acc.x
        if self.rect.top <= 0:
            self.rect.top = 0
            self.pos.y -= self.vel.y + 0.5 * self.acc.y
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.pos.y -= self.vel.y + 0.5 * self.acc.y

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super(Asteroid, self).__init__()
        self.image = pygame.Surface((0,0))
        self.surf = pygame.image.load("asteroid.png").convert()
        self.surf = pygame.transform.scale(self.surf, (40, 40))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 1)


    def update(self):
        self.rect.move_ip(-self.speed, 0)
        # Remove the sprite when it passes the left edge of the screen
        if self.rect.right < 0:
            self.kill()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, length):
        pygame.sprite.Sprite.__init__(self)
        self.image  = pygame.Surface((length, length))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.planet = random.randint(0,4)
        self.surf = PLANETS[self.planet].convert()
        self.surf = pygame.transform.scale(self.surf, (260, 260))
        self.surf.set_colorkey((0, 0, 1), RLEACCEL)



class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, length, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image  = pygame.Surface((length, length))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bars(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color, max_hp):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image  = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = max_hp
        self.max_hp = max_hp
        self.ratio = self.hp / self.max_hp
        global COOLDOWN
        self.ratio2 = COOLDOWN / 100



class Coins(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imageList = COIN_IMAGES
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = 10
        self.image = pygame.Surface((0,0))
        self.surf = self.imageList[self.imageIndex].convert()
        self.surf = pygame.transform.scale(self.surf, (50, 50))
        self.surf.set_colorkey((0, 0, 1), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.x= x
        self.rect.y=y
        self.points = 0



    def update(self):
        self.surf = self.imageList[self.imageIndex].convert()
        self.surf = pygame.transform.scale(self.surf, (50, 50))
        self.surf.set_colorkey((0, 0, 1), RLEACCEL)
        self.animationTimer += 1
        if self.animationTimer >= self.animationSpeed:
            self.animationTimer = 0
            self.imageIndex += 1
            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0






