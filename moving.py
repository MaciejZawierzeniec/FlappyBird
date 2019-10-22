import pygame as pg
import time
import random

pg.init()

display_width = 800
display_height = 600

gamedisplay = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('test')

black = (0, 0, 0)
white = (255, 255, 255)

clock = pg.time.Clock()
catImg = pg.image.load('cat.png')

cat_width = 67
cat_height = 123
cat_speed = 0
gameexit = False


class Movement():
    def __init__(self, y_change, event):
        self.y_change = y_change
        self.event = event

    def move(self):
        if self.event.type == pg.KEYDOWN:
            if self.event.key == pg.K_LEFT:
                self.x_change = -10
            elif self.event.key == pg.K_RIGHT:
               self. x_change = 10
        if self.event.type == pg.KEYUP:
            if self.event.key == pg.K_LEFT or self.event.key == pg.K_RIGHT:
                self.x_change = 0

    def jump(self):
        if self.event.type == pg.KEYDOWN:
            if self.event.key == pg.K_UP:
                self.y_change = +10
            elif self.event.key == pg.K_DOWN:
               self. x_change = -10
        if self.event.type == pg.KEYUP:
            if self.event.key == pg.K_LEFT or self.event.key == pg.K_RIGHT:
                self.x_change = 0

    def get_y_change(self):
        return self.y_change


''''Draws a cat'''


class Cat(Movement):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def display(self):
        gamedisplay.blit(catImg, (self.x, self.y))


class Pillar():
    def __init__(self, pillarx, pillary, pillarw, pillarh, color):
        self.pillarx = pillarx
        self.pillary = pillary
        self.pillarw = pillarw
        self.pillarh = pillarh
        self.color = color

    def place_pillar(self):
        pg.draw.rect(gamedisplay, self.color, [self.pillarx, self.pillary, self.pillarw, self.pillarh])


def text_objects(text, font):
    textsurface = font.render(text, True, black)
    return textsurface, textsurface.get_rect()


def display_message(text):
    largeText = pg.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gamedisplay.blit(TextSurf, TextRect)

    pg.display.update()

    time.sleep(2)

    game_loop()


def crash():
    display_message("You crashed")


def game_loop():
    global m
    global gameexit
    x = (display_width * 0.45)
    y = (display_height * 0.4)
    y_change = 0

    pillar_startx = 600
    pillar_starty = random.randrange(0, display_height)
    pillar_speed = 7
    pillar_width = 100
    pillar_height = 100

    while not gameexit:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameexit = True
            m = Movement(y_change, event)
            m.jump()

        y -= m.get_y_change()
        gamedisplay.fill(white)

        p = Pillar(pillar_startx, pillar_starty, pillar_width, pillar_height, black)
        p.place_pillar()
        pillar_startx -= pillar_speed
        c = Cat(x, y)
        c.display()

        if x > display_width - cat_width or x < 0:
            crash()

        if pillar_startx < 0 - pillar_width:
            pillar_startx = 600 + 2*pillar_width
            pillar_starty = random.randrange(0, display_height)

        if y > pillar_starty + pillar_height: # or y - cat_height > pillar_starty + pillar_height
            pass
        elif y + cat_height < pillar_starty:
            pass
        else:
            crash()

        pg.display.update()
        clock.tick(60)

if gameexit == False: game_loop()
pg.quit()
quit()