import pygame as pg
import time
import random
import math

display_width = 800
display_height = 600

pg.init()

gamedisplay = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('test')

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 200)

clock = pg.time.Clock()
birdImg = pg.image.load('bird.png')

bird_width = 32
bird_height = 32
game_exit = False


class Bird:
    startpos = 0
    jump_width = 160
    jump_height = 80
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


    #def start_falling
    def collision(self):
        for pillar in GeneratePillars.pillars_list:
            if self.y + bird_height < pillar.lpillary and\
                    self.y > pillar.upillary + pillar.pillar_height:
                pass
            else:
                if (self.x + bird_width > pillar.lpillarx >
                        self.x - GeneratePillars.pillar_width or
                        self.x + bird_width > pillar.upillarx >
                        self.x - GeneratePillars.pillar_width):
                    return True

    # > self.x >

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x


class Pillar:
    pillarsh = 0
    firstiteration = True
    color = green

    def __init__(self, upillarx, upillary, lpillarx,
                 lpillary, pillarw, pillar_height):
        self.upillarx = upillarx
        self.upillary = upillary
        self.lpillarx = lpillarx
        self.lpillary = lpillary
        self.pillarw = pillarw
        self.pillar_height = pillar_height

    def display_pillar(self):
        self.upillarx += self.pillarsh
        self.lpillarx += self.pillarsh

        pg.draw.rect(gamedisplay, self.color, [self.upillarx,
                                               self.upillary, self.pillarw, self.pillar_height])
        pg.draw.rect(gamedisplay, self.color, [self.lpillarx,
                                               self.lpillary, self.pillarw, self.pillar_height])

    def get_pillar_shift(self):
        return self.pillarsh

    def zero_shift(self):
        self.pillarsh = 0


class GeneratePillars:
    pillar_speed = 8
    pillar_width = 100
    pillar_height = 600
    lower_pillar_min_height = 1 / 3 * display_height
    i = 0
    pillars_list = []

    def __init__(self, quantity, lpillar_startx, lpillar_starty,
                 upillar_startx, upillar_starty):
        self.quantity = quantity
        self.lpillar_startx = lpillar_startx
        self.lpillar_starty = lpillar_starty
        self.upillar_startx = upillar_startx
        self.upillar_starty = upillar_starty

    def generate_pillars(self):

        for pillar in range(self.quantity):
            self.lpillar_startx = \
                (display_width + self.i * self.pillar_width +
                 (display_width - (self.quantity - 1) *
                  self.pillar_width) * self.i / self.quantity)

            self.upillar_startx = self.lpillar_startx

            if len(self.pillars_list) < self.quantity:
                self.pillars_list.append(Pillar(self.upillar_startx,
                                                self.upillar_starty,
                                                self.lpillar_startx,
                                                self.lpillar_starty,
                                                self.pillar_width,
                                                self.pillar_height, ))
                self.pillars_list[self.i].lpillary = \
                    random.randrange(self.lower_pillar_min_height, display_height)
                self.pillars_list[self.i].upillary = \
                    self.pillars_list[self.i].lpillary - 800

            if self.pillars_list[self.i].lpillarx <= 0 - self.pillar_width + self.pillar_speed \
                    and not self.pillars_list[self.i].firstiteration:
                self.pillars_list[self.i].lpillary = \
                    random.randrange(self.lower_pillar_min_height, display_height)
                self.pillars_list[self.i].upillary = \
                    self.pillars_list[self.i].lpillary - 800
            else:
                if self.pillars_list[self.i].firstiteration:
                    self.pillars_list[self.i].upillarx = self.upillar_startx
                    self.pillars_list[self.i].lpillarx = self.lpillar_startx
                else:
                    self.pillars_list[self.i].upillarx = display_width
                    self.pillars_list[self.i].lpillarx = display_width

            self.i += 1

        self.i = 0

    def refresh(self):
        self.pillars_list.clear()

    def display(self):
        for pillar in self.pillars_list:
            pillar.display_pillar()

    def move_pillars(self):
        for pillar in self.pillars_list:
            pillar.pillarsh -= self.pillar_speed

    def move_to_startpos(self):

        for pillar in self.pillars_list:
            if pillar.lpillarx + self.pillar_width <= 0:
                pillar.lpillarx = display_width
                pillar.lpillary = random.randrange(self.lower_pillar_min_height, display_height)

                pillar.upillarx = pillar.lpillarx
                pillar.upillary = pillar.lpillary - 800

                pillar.zero_shift()
                pillar.firstiteration = False

            self.i += 1

        self.i = 0


def text_objects(text, font):
    text_surface = font.render(text, True, red)
    return text_surface, text_surface.get_rect()


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
    global display_height
    x = (display_width * 0.1)
    y = (display_height * 0.65)
    jump = False

    pillar_speed = 8

    gp = GeneratePillars(3, display_width,
                         random.randrange(1, display_height),
                         display_width, random.randrange(1, display_height))
    gp.generate_pillars()

    bird = Bird(x, y, jump, pillar_speed)

    while not game_exit:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    bird._jump(jump=False)
                    jump = True

        if jump:
            bird._jump(jump)

        gamedisplay.fill(blue)

        gp.generate_pillars()
        gp.display()

        bird.display()

        gp.move_pillars()
        gp.move_to_startpos()

        if bird.collision():
            gp.refresh()
            crash()

        pg.display.update()
        clock.tick(60)


if not game_exit:
    game_loop()
pg.quit()
quit()