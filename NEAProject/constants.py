import pygame
pygame.init()



TITLE = 'Pynet'
#1000, 600
#1366, 768
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
font = pygame.font.SysFont('rage', 100)

hit_sound = pygame.mixer.Sound("hit.wav")
coincollected = pygame.mixer.Sound("coincollect.wav")
menu_music = pygame.mixer.Sound("menu.wav")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

#Player Properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.08
PLAYER_GRAV = 1
PLAYER_JUMP = 40
MAX_HEALTH = 100
COOLDOWN = 100

# x,y,size, color
PLATFORM_LIST = [(200, 350, 260),
                 (-200, 400, 260),
                 (1300, 450, 260),
                 (300, 700, 260),
                 (600, 100, 260),
                 (1100, 20, 260),
                 (900, 700, 260)]

PLANETS = [pygame.image.load('planets/planet1.png'),
               pygame.image.load('planets/planet2.png'),
               pygame.image.load('planets/planet3.png'),
               pygame.image.load('planets/planet4.png'),
               pygame.image.load('planets/planet5.png')]

COIN_LIST = [(305, 300),
             (500, 200)]

COIN_IMAGES = [pygame.image.load('coins/coin_0.png'),
               pygame.image.load('coins/coin_1.png'),
               pygame.image.load('coins/coin_2.png'),
               pygame.image.load('coins/coin_3.png'),
               pygame.image.load('coins/coin_4.png'),
               pygame.image.load('coins/coin_5.png')]

colours = [WHITE, GREEN, RED, BLUE]

BG = pygame.image.load('BG.jpg')
BG = pygame.transform.scale(BG, (SCREEN_WIDTH,SCREEN_HEIGHT))