import sys

import pygame
from pygame.locals import *


WIDTH, HEIGHT = 1280, 720
TANK_WIDTH, TANK_HEIGHT = 128, 128
PROJECTILE_WIDTH, PROJECTILE_HEIGHT = 12, 5
FPS = 60
GRASS_TILE = pygame.image.load("Assets/grass_tile.jpg")
TANK = pygame.transform.scale(
    pygame.image.load("Assets/tank.jpg"), (TANK_WIDTH, TANK_HEIGHT)
)
PROJECTILE_IMAGE = pygame.transform.scale(
    pygame.image.load("Assets/projectile.png"), (PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
)
TANK.set_colorkey((255, 255, 255))

TILE_MAP = [
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
]
GRASS_SIZE = 256


class CycleList:
    def __init__(self):
        self.directions = ["top", "left", "bottom", "right"]

        self.last = ""

    def next(self, last):
        if last == "" or last == "right":
            self.directions = [self.directions[-1]] + self.directions[:3]
        elif last == "left":
            self.directions = self.directions[1:] + [self.directions[0]]

    def get_current(self):
        return self.directions[0]


class Projectile:
    def __init__(self, start_coordinates, image):
        self.rect = pygame.rect.Rect(*start_coordinates, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
        self.image = image

    def fly(self, direction):
        if direction == "top":
            self.rect.y -= 10
        if direction == "bottom":
            pygame.transform.rotate(self.image, 180)
            self.rect.y += 10
        if direction == "left":
            pygame.transform.rotate(self.image, 90)
            self.rect.x -= 10
        if direction == "right":
            pygame.transform.rotate(self.image, -90)
            self.rect.x += 10

        if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y > HEIGHT or self.rect.y < 0:
            return True


class Tank:
    def __init__(self, start_position, image, ammo):
        self.rect = pygame.rect.Rect(*start_position, TANK_WIDTH, TANK_HEIGHT)
        self.image = image
        self.directions = CycleList()
        self.last = ""
        self.ammo = []
        self.ammo_counter = 0

        self.clock = pygame.time.Clock()

    def get_coordinates(self):
        return self.rect.x, self.rect.y

    def fire(self):
        if self.ammo_counter < 24:
            self.ammo.append(Projectile((self.rect.x + (TANK_WIDTH - PROJECTILE_WIDTH) // 2,
                                         self.rect.y + (TANK_HEIGHT - PROJECTILE_HEIGHT) // 2),
                                        PROJECTILE_IMAGE))

            self.ammo_counter += 1

    def move(self, speed, direction):
        if direction == "left":
            self.rect.x -= speed
        if direction == "right":
            self.rect.x += speed
        if direction == "top":
            self.rect.y -= speed
        if direction == "bottom":
            self.rect.y += speed

    def rotate(self, direction):
        if direction == "right":
            self.image = pygame.transform.rotate(self.image, -90)

            self.directions.next(self.last)

            self.last = "right"

        if direction == "left":
            self.image = pygame.transform.rotate(self.image, 90)

            self.directions.next(self.last)

            self.last = "left"


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.directions = CycleList()

        self.tank = Tank((250, 250), TANK, 24)

        pygame.display.set_caption("Танчики")

    def background(self):
        for i, row in enumerate(TILE_MAP):
            for j, item in enumerate(row):
                if item == 1:
                    self.screen.blit(GRASS_TILE, (j * GRASS_SIZE, i * GRASS_SIZE))

    def run(self):
        while True:
            self.background()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_d:
                        self.tank.rotate("right")
                        self.directions.next("right")

                    if event.key == K_a:
                        self.tank.rotate("left")
                        self.directions.next("left")

                    if event.key == K_SPACE:
                        self.tank.fire()

            self.screen.blit(self.tank.image, self.tank.get_coordinates())

            if pygame.key.get_pressed()[K_w]:
                self.tank.move(2, self.directions.get_current())

            for projectile in self.tank.ammo:
                projectile.fly(self.directions.get_current())
                self.screen.blit(projectile.image, (projectile.rect.x, projectile.rect.y))

            pygame.display.update()
            self.clock.tick()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
