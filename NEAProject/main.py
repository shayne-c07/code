import importlib
import time
import pygame
import random
import pymunk
from pymunk import Vec2d

from sprites import *
from constants import *

import pymunk as pm




# Create the screen object`

# Create a custom event for adding a new asteroid
ADDASTEROID = pygame.USEREVENT + 1

pygame.time.set_timer(ADDASTEROID, 1500)

REGEN = pygame.USEREVENT +2
pygame.time.set_timer(REGEN, 3000)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pynet: Space Platformer')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True




    def new(self):
        self.health = 100
        self.points = 0
        self.maxpoints = 15


        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.bars =pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.player = slimePlayer(self)
        self.asteroid = Asteroid()

        self.all_sprites.add(self.player)
        self.all_sprites.add(self.asteroid)

        for n in range(3000):
            x = random.randint(-4000, 4000)
            y = random.randint(-2000, 2000)
            size = random.randint(1,5)
            colour = random.choice(colours)
            star = Star(x, y, size, colour)
            self.all_sprites.add(star)
            self.stars.add(star)

        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        for n in range(5):
            x = random.randint(-1500, 1500)
            y = random.randint(-900, 900)
            n = Platform(x, y, 260)
            self.all_sprites.add(n)
            self.platforms.add(n)

        for c in range(self.maxpoints):
            x = random.randint(-1000, 1000)
            y = random.randint(-600, 600)
            c = Coins(x, y)
            self.all_sprites.add(c)
            self.coins.add(c)

        self.run()



    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        self.ratio = self.health / MAX_HEALTH
        health_bar = Bars(10, SCREEN_HEIGHT - 40, 150, 20, RED, MAX_HEALTH)
        health_bar2 = Bars(10, SCREEN_HEIGHT - 40, 150 * self.ratio, 20, GREEN, MAX_HEALTH)
        fuel_bar = Bars(200, SCREEN_HEIGHT - 40, 150, 20, WHITE, MAX_HEALTH)
        fuel_bar2 = Bars(200, SCREEN_HEIGHT - 40, 150 * (fuel_bar.ratio2), 20, YELLOW, MAX_HEALTH)
        self.bars.add(health_bar, health_bar2, fuel_bar, fuel_bar2)

        # new border validation
        self.total = 0
        for plat in self.platforms:
            if plat.rect.y < -1000 or plat.rect.x <-2000 or plat.rect.x >2000:
                self.total = self.total+1
                if self.total >= len(self.platforms) - 1:
                    self.show_lose_screen()

        #update sprites
        self.all_sprites.update()

        #Keep player on platform
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if hits and self.player.vel.y >= 0:
            # if self.player.pos.y < hits[0].rect.bottom:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 0



        # Screen Scrolling
        if self.player.rect.top < SCREEN_HEIGHT*0.5:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
            for asteroids in self.asteroids:
                asteroids.rect.y += abs(self.player.vel.y)
            for stars in self.stars:
                stars.rect.y += abs(self.player.vel.y / 4)
            for coins in self.coins:
                coins.rect.y += abs(self.player.vel.y)
        if self.player.rect.top >= SCREEN_HEIGHT*0.5:
            self.player.pos.y -= abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y -= abs(self.player.vel.y)
            for asteroids in self.asteroids:
                asteroids.rect.y -= abs(self.player.vel.y)
            for stars in self.stars:
                stars.rect.y -= abs(self.player.vel.y / 4)
            for coins in self.coins:
                coins.rect.y -= abs(self.player.vel.y)
        if self.player.rect.centerx >= SCREEN_WIDTH*0.5:
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)
            for asteroids in self.asteroids:
                asteroids.rect.x -= abs(self.player.vel.x)
            for stars in self.stars:
                stars.rect.x -= abs(self.player.vel.x / 4)
            for coins in self.coins:
                coins.rect.x -= abs(self.player.vel.x)
        if self.player.rect.centerx < SCREEN_WIDTH*0.5:
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x)
            for asteroids in self.asteroids:
                asteroids.rect.x += abs(self.player.vel.x)
            for stars in self.stars:
                stars.rect.x += abs(self.player.vel.x / 4)
            for coins in self.coins:
                coins.rect.x += abs(self.player.vel.x)


                # asteroid collision
        asteroid_hit = pygame.sprite.spritecollide(self.player, self.asteroids, True)
        if asteroid_hit:
            pygame.mixer.Sound.play(hit_sound)
            self.player.vel.x = -15
            self.player.surf = pygame.image.load("angryslime.png").convert()
            self.player.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.health -= 20
            if self.health <= 0:
                self.show_lose_screen()

        #coin obtaining#
        coin_got = pygame.sprite.spritecollide(self.player, self.coins, True)
        if coin_got:
            self.points +=1
            pygame.mixer.Sound.play(coincollected)

            if self.points == self.maxpoints:
                self.show_win_screen()




        self.asteroids.update()



    def events(self):
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                #options menu#
                if event.key == K_p:
                    self.pause()
                if event.key == pygame.K_SPACE:
                    self.player.jump()
            elif event.type == QUIT:
                g.running = False
                g.playing = False
            elif event.type == ADDASTEROID:
                # Create the new asteroid and add it to sprite groups
                new_asteroid = Asteroid()
                self.asteroids.add(new_asteroid)
                self.all_sprites.add(new_asteroid)
            elif event.type == REGEN:
                if self.health <100:
                    self.health += 5



    def draw(self):
        # self.screen.blit(BG, (0, 0))
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        for planet in self.platforms:
            self.screen.blit(planet.surf, planet.rect)
        self.screen.blit(self.player.surf, self.player.rect)
        for entity in self.asteroids:
            self.screen.blit(entity.surf, entity.rect)
        for coin in self.coins:
            self.screen.blit(coin.surf, coin.rect)
        self.bars.draw(self.screen)

        #coin at the top
        topcoin = pygame.image.load('coins/coin_0.png')
        topcoin = pygame.transform.scale(topcoin, (50, 50))
        topcoin.set_colorkey((0, 0, 1), RLEACCEL)
        self.screen.blit(topcoin, (17,5))
        self.draw_text(f'x{self.points}', pygame.font.SysFont('snapitc', 50), (WHITE), g.screen,75, -2)
        health = f'{self.health}/{MAX_HEALTH}'
        self.draw_text(health, pygame.font.SysFont('calibri', 20), WHITE, self.screen, 5, SCREEN_HEIGHT-20)
        self.draw_text('FUEL', pygame.font.SysFont('calibri', 20), WHITE, self.screen, 200, SCREEN_HEIGHT-20)




        pygame.display.flip()



    def show_win_screen(self):
        win = True

        while win:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        importlib.import_module('menu')


            self.screen.fill(BLACK)
            self.draw_text("YOU WON!", pygame.font.SysFont('aguda', 130), "yellow", g.screen, 250, 100)
            self.draw_text("Press ESC to return to the main menu", pygame.font.SysFont('calibri', 30), (WHITE), g.screen,
                           300, 300)
            pygame.display.update()
            self.clock.tick(5)

    def show_lose_screen(self):
        over = True
        while over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        importlib.import_module('menu')
                    elif event.key == K_r:
                        over = False
                        self.new()

            self.screen.fill(BLACK)
            self.draw_text("YOU DIED", pygame.font.SysFont('aguda', 130), (WHITE), g.screen, 250, 100)
            self.draw_text("Press R to restart or ESC to quit", pygame.font.SysFont('calibri', 30), (WHITE), g.screen,
                           300, 300)
            pygame.display.update()
            self.clock.tick(5)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x,y)
        surface.blit(textobj, textrect)

    def pause(self):
        paused = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        paused = False
                    elif event.key == K_ESCAPE:
                        importlib.import_module('menu')

            self.screen.blit(BG, (0, 0))
            self.draw_text("Game Paused", pygame.font.SysFont('aguda', 130), (WHITE), g.screen, 250, 100)
            self.draw_text("Press P to unpause or ESC to quit", pygame.font.SysFont('calibri', 30), (WHITE), g.screen, 300, 200)
            pygame.display.update()
            self.clock.tick(5)






running = True

g = Game()
# Main loop
while g.running:
    g.new()



