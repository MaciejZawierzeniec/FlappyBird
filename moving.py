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

cat_width = 59
cat_height = 96
cat_speed = 0
gameexit = False


class Movement():
    def __init__(self, y_change, event):
        self.y_change = y_change
        self.event = event

    def jump(self):
        if self.event.type == pg.KEYDOWN:
            if self.event.key == pg.K_UP:
                self.y_change = +10
            elif self.event.key == pg.K_DOWN:
                self.y_change = -10
        if self.event.type == pg.KEYUP:
            if self.event.key == pg.K_UP or self.event.key == pg.K_DOWN:
                self.x_change = 0

    def get_y_change(self):
        return self.y_change


'''Draws a cat'''


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
    largeText = pg.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
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

    pillar_speed = 7

    lpillar_startx = 800
    lpillar_starty = random.randrange(350, display_height)
    lpillar_width = 150
    lpillar_height = 600

    upillar_startx = 800
    upillar_starty = lpillar_starty - 850
    upillar_width = 150
    upillar_height = 600

    while not gameexit:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameexit = True
            m = Movement(y_change, event)
            m.jump()

        y -= m.get_y_change()
        gamedisplay.fill(white)

        low = Pillar(lpillar_startx, lpillar_starty, lpillar_width, lpillar_height, black)
        low.place_pillar()
        up = Pillar(upillar_startx, upillar_starty, upillar_width, upillar_height, black)
        up.place_pillar()

        lpillar_startx -= pillar_speed
        upillar_startx -= pillar_speed

        c = Cat(x, y)
        c.display()

        if lpillar_startx < 0 - lpillar_width:
            lpillar_startx = 600 + 2 * lpillar_width
            lpillar_starty = random.randrange(350, display_height)
        if upillar_startx < 0 - upillar_width:
            upillar_startx = 600 + 2 * upillar_width
            upillar_starty = lpillar_starty - 850

        if y + cat_height > lpillar_starty or y < upillar_starty + upillar_height:
            if (x + cat_width > lpillar_startx and x < lpillar_startx + lpillar_width or
                    x + cat_width > upillar_startx and x < upillar_startx + upillar_width):
                crash()

        pg.display.update()
        clock.tick(60)


if gameexit == False: game_loop()
pg.quit()
quit()
