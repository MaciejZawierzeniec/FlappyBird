import pygame as pg
import time
import random
import math

display_width = 800
display_height = 600

pg.init()

gameDisplay = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('Flappy Bird')

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 200)

clock = pg.time.Clock()
birdImg = pg.image.load('bird.png')

bird_width = 32
bird_height = 32
game_exit = False


class Bird:
    start_position = 0
    jump_width = 160
    jump_height = 80
    points = 0
    y_change = 0
    up = True
    X_SHIFT = -(math.sqrt(-4 * (1 / jump_width) * (-jump_height))) / (2 * (1 / jump_width))

    def __init__(self, x, y, is_jumping, tube_speed):
        self.x = x
        self.y = y
        self.is_jumping = is_jumping
        self.tube_speed = tube_speed
        self.x_shift = self.X_SHIFT

    def display(self):
        gameDisplay.blit(birdImg, (self.x, self.y))

    def jump(self, is_jumping):
        self.is_jumping = is_jumping

        if not self.is_jumping:
            self.start_position = self.y
            self.is_jumping = True
            self.x_shift = self.X_SHIFT

        self.y = (self.start_position + (1 / self.jump_width) *
                  self.x_shift ** 2 - self.jump_height)
        self.x_shift += self.tube_speed

    def collision(self):
        for tube in TubeManagement.tubes:
            if self.y + bird_height < tube.lower_tube_y and \
                    self.y > tube.upper_tube_y + tube.tube_height:
                if tube.upper_tube_x == self.x:
                    self.points += 1
            else:
                if (self.x + bird_width > tube.lower_tube_x >
                        self.x - TubeManagement.tube_width or
                        self.x + bird_width > tube.upper_tube_x >
                        self.x - TubeManagement.tube_width):
                    self.points = 0
                    return True

    def get_points(self):
        return self.points


class Tube:
    tube_shift = 0
    first_iteration = True
    color = green

    def __init__(self, upper_tube_x, upper_tube_y, lower_tube_x, lower_tube_y, tube_width, tube_height):
        self.upper_tube_x = upper_tube_x
        self.upper_tube_y = upper_tube_y
        self.lower_tube_x = lower_tube_x
        self.lower_tube_y = lower_tube_y
        self.tube_width = tube_width
        self.tube_height = tube_height

    def display_tube(self):
        self.upper_tube_x += self.tube_shift
        self.lower_tube_x += self.tube_shift

        pg.draw.rect(gameDisplay, self.color, [self.upper_tube_x, self.upper_tube_y, self.tube_width, self.tube_height])
        pg.draw.rect(gameDisplay, self.color, [self.lower_tube_x, self.lower_tube_y, self.tube_width, self.tube_height])

    def zero_shift(self):
        self.tube_shift = 0


class TubeManagement(Tube):
    tube_speed = 8
    tube_width = 100
    tube_height = 600
    lower_tube_min_height = 1 / 3 * display_height
    i = 0
    tubes = []

    def __init__(self, quantity, lower_tube_x, lower_tube_y, upper_tube_x, upper_tube_y):
        super().__init__(upper_tube_x, upper_tube_y, lower_tube_x, lower_tube_y, self.tube_width, self.tube_height)
        self.quantity = quantity

    def generate_tubes(self):
        for self.i in range(self.quantity):
            self._get_equal_tube_x_distances()

            if len(self.tubes) < self.quantity:
                self._create_tubes_pair()

            if self.tubes[self.i].first_iteration:
                self.tubes[self.i].upper_tube_x = self.upper_tube_x
                self.tubes[self.i].lower_tube_x = self.lower_tube_x
            else:
                self.tubes[self.i].upper_tube_x = display_width
                self.tubes[self.i].lower_tube_x = display_width

    def _get_equal_tube_x_distances(self):
        self.lower_tube_x = (display_width + self.i * self.tube_width + (display_width -
                            (self.quantity - 1) * self.tube_width) * self.i / self.quantity)
        self.upper_tube_x = self.lower_tube_x

    def _create_tubes_pair(self):
        self.tubes.append(Tube(self.upper_tube_x,
                               self.upper_tube_y,
                               self.lower_tube_x,
                               self.lower_tube_y,
                               self.tube_width,
                               self.tube_height))
        self.tubes[self.i].lower_tube_y = random.randrange(int(self.lower_tube_min_height), display_height)
        self.tubes[self.i].upper_tube_y = self.tubes[self.i].lower_tube_y - 800

    def refresh(self):
        self.tubes.clear()

    def display(self):
        for tube in self.tubes:
            tube.display_tube()

    def move_tubes(self):
        for tube in self.tubes:
            tube.tube_shift -= self.tube_speed

    def restart_position(self):
        for tube in self.tubes:
            if tube.lower_tube_x + self.tube_width <= 0:
                tube.lower_tube_x = display_width
                tube.lower_tube_y = random.randrange(round(self.lower_tube_min_height), display_height)
                tube.upper_tube_x = tube.lower_tube_x
                tube.upper_tube_y = tube.lower_tube_y - 800
                tube.zero_shift()
                tube.first_iteration = False


def text_objects(text, font):
    text_surface = font.render(text, True, red)
    return text_surface, text_surface.get_rect()


def display_message(text):
    large_text = pg.font.Font('freesansbold.ttf', 115)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(text_surf, text_rect)

    pg.display.update()
    time.sleep(2)
    game_loop()


def display_points(text):
    large_text = pg.font.Font('freesansbold.ttf', 20)
    text_surf, text_rect = text_objects("Points: " + text, large_text)
    text_rect.center = ((display_width - 60), (display_height / 20))
    gameDisplay.blit(text_surf, text_rect)

    pg.display.update()


def crash():
    display_message("You crashed")


def game_loop():
    global game_exit
    global display_height
    bird_start_x = (display_width * 0.1)
    bird_start_y = (display_height * 0.65)
    _jump = False
    tube_speed = 8

    gt = TubeManagement(3, display_width,
                        random.randrange(1, display_height),
                        display_width, random.randrange(1, display_height))
    gt.generate_tubes()

    bird = Bird(bird_start_x, bird_start_y, _jump, tube_speed)

    while not game_exit:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    bird.jump(False)
                    _jump = True

        if _jump:
            bird.jump(_jump)

        gameDisplay.fill(blue)

        gt.generate_tubes()
        gt.display()
        bird.display()
        gt.move_tubes()
        gt.restart_position()

        if bird.collision():
            gt.refresh()
            crash()
        display_points(str(bird.get_points()))

        pg.display.update()
        clock.tick(60)


if not game_exit:
    game_loop()
pg.quit()
quit()
