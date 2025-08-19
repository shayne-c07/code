import pygame
from random import uniform, randint
from constants import *
import importlib
from pygame.locals import *
import pygame_functions as f


pygame.init()

CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.mixer.init()
pygame.mixer.music.load('menu.wav')
pygame.mixer.music.play(-1)
volume = 1

title_font = pygame.font.SysFont('rage', 100)
options_font = pygame.font.SysFont('calibri', 40)

class Button:
    def __init__(self,image, x, y, page):
        self.img = image
        self.page= page
        self.rect = self.img.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):
        mousepos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousepos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                if self.page == 'main':
                    importlib.import_module(self.page)
                if self.page == 'options':
                    global running
                    running = False
                    options_menu()
                if self.page == 'selector':
                    #load level selector
                    pass


                # import module
            if not pygame.mouse.get_pressed()[0]:
                self.clicked= False

        screen.blit(self.img, (self.rect.x, self.rect.y))


class Slider:
    def __init__(self, pos: tuple, size: tuple, inital, min, max):
        self.pos= pos
        self.size= size

        self.slider_left_pos = self.pos[0] - (size[0]//2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max
        self.initial = (self.slider_right_pos - self.slider_left_pos) * inital

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial - 10, self.slider_top_pos, 20, self.size[1])

    def draw(self, screen):
        pygame.draw.rect(screen, "darkgray", self.container_rect)
        pygame.draw.rect(screen, "blue", self.button_rect)


    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val =self.button_rect.centerx - self.slider_left_pos

        return(button_val / val_range)
              # *(self.max - self.min) + self.min





start_img = pygame.image.load("start.png")
start_img = pygame.transform.scale(start_img, (400,400))

options_img = pygame.image.load("options.png")
options_img = pygame.transform.scale(options_img, (200,200))

selector_img = pygame.image.load("selector.png")
selector_img = pygame.transform.scale(selector_img, (180,200))


start= Button(start_img, 315, 75, 'main')
options = Button(options_img, 100, 350, 'options')
selector  = Button(selector_img, 700, 300, 'selector')

sliders = [
    Slider((SCREEN_WIDTH/2, 200), (150, 40), 0.5, 0, 100)
]



def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

def main_menu():
    pygame.display.set_caption('Pynet: Space Platformer')

    draw_text('PYNET', title_font, ((WHITE)), screen, 340, 50)
    draw_text('Start Game', pygame.font.SysFont('consolas', 30), (BLACK), screen, SCREEN_WIDTH / 2 - 70, 250)
    draw_text('Options', pygame.font.SysFont('consolas', 30), (BLACK), screen, SCREEN_WIDTH / 2 - 350, 430)
    draw_text('Level Selector', pygame.font.SysFont('consolas', 17), (BLACK), screen, SCREEN_WIDTH / 2 + 225, 380)


def options_menu():
    running = True







    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        screen.fill(BLACK)
        screen.blit(BG, (0, 0))

        draw_text('options', title_font, (WHITE), screen, 20, 5)
        draw_text('Music Volume', options_font , (WHITE), screen, 20, 180)
        draw_text('Coin Number', options_font, WHITE, screen, 20, 360)
        draw_text('Press ESC to go back', options_font, WHITE, screen, 650, SCREEN_HEIGHT-50)



        for slider in sliders:
            if slider.container_rect.collidepoint(mouse_pos) and mouse[0]:
                slider.move_slider(mouse_pos)
            slider.draw(screen)


        volume = sliders[0].get_value()
        pygame.mixer.music.set_volume(volume)
        draw_text(f'{int(volume *100)}', pygame.font.SysFont('calibri', 20), (WHITE), screen, 600, 190)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.flip()
        CLOCK.tick(FPS)








running = True
screen.fill((0, 0, 0))

while running:
    screen.blit(BG, (0, 0))



    start.draw()
    options.draw()
    selector.draw()



    main_menu()

    running = True

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            # print(pygame.title_font.get_fonts())
            running = False
    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()