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
game_exit = False


class Bird:
    startpos = 0
    jump_width = 160
    jump_height = 160
    x_change = -(math.sqrt(-4 * (1 / jump_width) * (-jump_height))) / (2 * (1 / jump_width))
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
            self.x_change = -(math.sqrt(-4 * (1 / self.jump_width) * (-self.jump_height))) / (2 * (1 / self.jump_width))

        self.y = self.startpos + (1 / self.jump_width) * self.x_change * self.x_change - self.jump_height
        self.x_change += self.pillar_speed

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x


class Pillar(Bird):

    def __init__(self, pillarx, pillary, pillarw, pillarh, color):
        self.pillarx = pillarx
        self.pillary = pillary
        self.pillarw = pillarw
        self.pillarh = pillarh
        self.color = color

    def place_pillar(self):
        pg.draw.rect(gamedisplay, self.color, [self.pillarx, self.pillary, self.pillarw, self.pillarh])

    def collision(self, x, y):
        if y + bird_height > self.pillary or y < self.pillary + self.pillarh:
            if (x + bird_width > self.pillarx and x < self.pillarx + self.pillarw or
                    x + bird_width > self.pillarx and x < self.pillarx + self.pillarw):
                crash()



def text_objects(text, font):
    textsurface = font.render(text, True, black)
    return textsurface, textsurface.get_rect()


def display_message(text):
    largetext = pg.font.Font('freesansbold.ttf', 115)
    textsurf, textrect = text_objects(text, largetext)
    textrect.center = ((display_width / 2), (display_height / 2))
    gamedisplay.blit(textsurf, textrect)

    pg.display.update()

    time.sleep(2)

    game_loop()


def crash():
    display_message("You crashed")


def game_loop():
    global game_exit
    x = (display_width * 0.1)
    y = (display_height * 0.65)
    jump = False

    pillar_speed = 8
    pillar_width = 100
    pillar_height = 600

    lpillar_startx = display_width
    lpillar_starty = random.randrange(350, display_height)

    lpillar2_startx = display_width + pillar_width + (display_width - 2 * pillar_width) * 1/3
    lpillar2_starty = random.randrange(350, display_height)

    lpillar3_startx = display_width + 2*pillar_width + (display_width - 2 * pillar_width) * 2/3
    lpillar3_starty = random.randrange(350, display_height)


    upillar_startx = lpillar_startx
    upillar_starty = lpillar_starty - 800

    upillar2_startx = lpillar2_startx
    upillar2_starty = lpillar2_starty - 800

    upillar3_startx = lpillar3_startx
    upillar3_starty = lpillar3_starty - 800

    c = Bird(x, y, jump, pillar_speed)

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

        low = Pillar(lpillar_startx, lpillar_starty, pillar_width, pillar_height, black)
        low.place_pillar()

        low2 = Pillar(lpillar2_startx, lpillar2_starty, pillar_width, pillar_height, black)
        low2.place_pillar()

        low3 = Pillar(lpillar3_startx, lpillar3_starty, pillar_width, pillar_height, black)
        low3.place_pillar()

        up = Pillar(upillar_startx, upillar_starty, pillar_width, pillar_height, black)
        up.place_pillar()

        up2 = Pillar(upillar2_startx, upillar2_starty, pillar_width, pillar_height, black)
        up2.place_pillar()

        up3 = Pillar(upillar3_startx, upillar3_starty, pillar_width, pillar_height, black)
        up3.place_pillar()

        c.display()

        if lpillar_startx + pillar_width < 0:
            lpillar_startx = display_width
            lpillar_starty = random.randrange(350, display_height)
        if upillar_startx < 0 - pillar_width:
            upillar_startx = lpillar_startx
            upillar_starty = lpillar_starty - 800

        if lpillar2_startx + pillar_width < 0:
            lpillar2_startx = display_width
            lpillar2_starty = random.randrange(350, display_height)
        if upillar2_startx < 0 - pillar_width:
            upillar2_startx = lpillar2_startx
            upillar2_starty = lpillar2_starty - 800

        if lpillar3_startx + pillar_width < 0:
            lpillar3_startx = display_width
            lpillar3_starty = random.randrange(350, display_height)
        if upillar3_startx < 0 - pillar_width:
            upillar3_startx = lpillar3_startx
            upillar3_starty = lpillar3_starty - 800

        lpillar_startx -= pillar_speed
        lpillar2_startx -= pillar_speed
        lpillar3_startx -= pillar_speed

        upillar_startx -= pillar_speed
        upillar2_startx -= pillar_speed
        upillar3_startx -= pillar_speed

        low2.collision(c.get_x(), c.get_y())
        if c.get_y() + bird_height > lpillar_starty or c.get_y() < upillar_starty + pillar_height:
            if (x + bird_width > lpillar_startx and x < lpillar_startx + pillar_width or
                    x + bird_width > upillar_startx and x < upillar_startx + pillar_width):
                crash()

        pg.display.update()
        clock.tick(60)


if not game_exit:
    game_loop()
pg.quit()
quit()
