import pygame as pg
import time
import random
import math


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


class Bird:
    startpos = 0
    jump_width = 160
    jump_height = 160
    x_change = -(math.sqrt(-4 * (1 / jump_width) *
                 (-jump_height))) / (2 * (1 / jump_width))
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
            self.x_change = (-(math.sqrt(-4 * (1 / self.jump_width) *
                             (-self.jump_height))) /
                             (2 * (1 / self.jump_width)))

        self.y = (self.startpos + (1 / self.jump_width) *
                  self.x_change * self.x_change - self.jump_height)
        self.x_change += self.pillar_speed

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x


class Pillar:

    pillarsh = 0
    firstiteration = True

    def __init__(self, upillarx, upillary, lpillarx,
                 lpillary, pillarw, pillarh, color):
        self.upillarx = upillarx
        self.upillary = upillary
        self.lpillarx = lpillarx
        self.lpillary = lpillary
        self.pillarw = pillarw
        self.pillarh = pillarh
        self.color = color

    def display_pillar(self):
        self.upillarx += self.pillarsh
        self.lpillarx += self.pillarsh

        pg.draw.rect(gamedisplay, self.color, [self.upillarx,
                     self.upillary, self.pillarw, self.pillarh])
        pg.draw.rect(gamedisplay, self.color, [self.lpillarx,
                     self.lpillary, self.pillarw, self.pillarh])


class GeneratePillars:
    pillar_speed = 8
    pillar_width = 100
    pillar_height = 600
    actu = 0
    pillar = []
    color = black

    def __init__(self, quantity, lpillar_startx, lpillar_starty,
                 upillar_startx, upillar_starty):
        self.quantity = quantity
        self.lpillar_startx = lpillar_startx
        self.lpillar_starty = lpillar_starty
        self.upillar_startx = upillar_startx
        self.upillar_starty = upillar_starty

    def generate_pillars(self):

        for pillar in range(self.quantity):
            self.lpillar_startx = (display_width + self.actu * self.pillar_width + (display_width -
                                   (self.quantity - 1) * self.pillar_width) * self.actu / self.quantity)

            if self.lpillar_startx + self.pillar_width < 0:
                self.lpillar_starty = random.randrange(350, display_height)

            self.upillar_startx = self.lpillar_startx
            self.upillar_starty = self.lpillar_starty - 800

            if len(self.pillar) < self.quantity:
                self.pillar.append(Pillar(self.upillar_startx,
                                          self.upillar_starty,
                                          self.lpillar_startx,
                                          pillar, self.pillar_width,
                                          self.pillar_height,
                                          self.color))
            elif len(self.pillar) == self.quantity:
                if self.pillar[self.actu].firstiteration:
                    self.pillar[self.actu].upillarx = self.upillar_startx
                    self.pillar[self.actu].upillary = self.upillar_starty
                    self.pillar[self.actu].lpillarx = self.lpillar_startx
                    self.pillar[self.actu].lpillary = self.lpillar_starty
                else:
                    self.pillar[self.actu].upillarx = display_width
                    self.pillar[self.actu].upillary = self.upillar_starty
                    self.pillar[self.actu].lpillarx = display_width
                    self.pillar[self.actu].lpillary = self.lpillar_starty

            self.actu += 1

        self.actu = 0

    def displ(self):
        for pillar in self.pillar:
            pillar.display_pillar()

    def move_pillars(self):
        for pillar in self.pillar:
            pillar.pillarsh -= self.pillar_speed

    def move_to_startpos(self):

        for pillar in self.pillar:
            if pillar.lpillarx + self.pillar_width < 0:
                pillar.lpillarx = display_width
                pillar.lpillary = random.randrange(350, display_height)

                pillar.upillarx = pillar.lpillarx
                pillar.upillary = pillar.lpillary - 800

                pillar.pillarsh = 0
                pillar.firstiteration = False

            self.actu += 1

        self.actu = 0


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
    global gameexit
    x = (display_width * 0.1)
    y = (display_height * 0.65)
    jump = False

    pillar_speed = 8

    gp = GeneratePillars(3, display_width,
                         random.randrange(350, display_height),
                         display_width, random.randrange(350, display_height))
    gp.generate_pillars()

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

        gp.generate_pillars()
        gp.displ()

        c.display()

        gp.move_to_startpos()

        gp.move_pillars()

        '''
        if c.get_y() + bird_height > lpillar_starty or c.get_y() < upillar_starty + pillar_height:
            if (x + bird_width > lpillar_startx and x < lpillar_startx + pillar_width or
                    x + bird_width > upillar_startx and x < upillar_startx + pillar_width):
                crash()
        '''

        pg.display.update()
        clock.tick(60)


if not gameexit:
    game_loop()
pg.quit()
quit()
