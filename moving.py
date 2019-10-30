import pygame as pg
import time
import random
import math

pg.init()

display_width = 800
display_height = 600

gamedisplay = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('test')

black = (0, 0, 0)
white = (255, 255, 255)

clock = pg.time.Clock()
birdImg = pg.image.load('bird.png')

bird_width = 32
bird_height = 32
gameexit = False




'''Draws a bird'''


class bird():

    startpos = 0
    jump_width = 350
    jump_height = 200
    x_change = -(math.sqrt(-4*(1/jump_width)*(-jump_height)))/(2*(1/jump_width))
    y_change = 0
    up = True

    def __init__(self, x, y, jump, pillar_speed):
        self.x = x
        self.y = y
        self.jump = jump
        self.pillar_speed = pillar_speed

    def display(self):
        gamedisplay.blit(birdImg, (self.x, self.y))

    def _jump(self, jump):
        self.jump = jump

        if not self.jump:
            self.startpos = self.y
            self.jump = True
            self.x_change = -(math.sqrt(-4*(1/self.jump_width)*(-self.jump_height)))/(2*(1/self.jump_width))
        print("xchange ", (math.sqrt(-4*(1/self.jump_width)*(-self.jump_height)))/(2*(1/self.jump_width)))
        self.y = self.startpos + (1 / self.jump_width) * self.x_change * self.x_change - self.jump_height
        self.x_change += self.pillar_speed
        print(self.y)


    def get_y(self):
        return self.y


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
    x = (display_width * 0.1)
    y = (display_height * 0.65)
    jump = False

    pillar_speed = 8

    lpillar_startx = 800
    lpillar_starty = random.randrange(350, display_height)
    lpillar_width = 150
    lpillar_height = 600

    upillar_startx = 800
    upillar_starty = lpillar_starty - 800
    upillar_width = 150
    upillar_height = 600

    c = bird(x, y, jump, pillar_speed)

    while not gameexit:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameexit = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    c._jump(jump=False)
                    jump = True

        if jump:
            c._jump(jump)

        gamedisplay.fill(white)

        low = Pillar(lpillar_startx, lpillar_starty, lpillar_width, lpillar_height, black)
        low.place_pillar()
        up = Pillar(upillar_startx, upillar_starty, upillar_width, upillar_height, black)
        up.place_pillar()

        lpillar_startx -= pillar_speed
        upillar_startx -= pillar_speed

        #c = bird(x, y)
        c.display()

        if lpillar_startx < 0 - lpillar_width:
            lpillar_startx = 600 + 2 * lpillar_width
            lpillar_starty = random.randrange(250, display_height - 250)
        if upillar_startx < 0 - upillar_width:
            upillar_startx = 600 + 2 * upillar_width
            upillar_starty = lpillar_starty - 850

        if c.get_y() + bird_height > lpillar_starty or c.get_y() < upillar_starty + upillar_height:
            if (x + bird_width > lpillar_startx and x < lpillar_startx + lpillar_width or
                    x + bird_width > upillar_startx and x < upillar_startx + upillar_width):
                crash()

        pg.display.update()
        clock.tick(60)


if gameexit == False: game_loop()
pg.quit()
quit()
