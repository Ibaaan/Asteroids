# размеры экрана
import pygame

HEIGHT = 600
WIDTH = 800

# константы для корабля
SHIP_MAX_VELOCITY = 2.7
SHIP_ANGULAR_VELOCITY = 4
CLOCKWISE = True
COUNTER_CLOCKWISE = False
# коэффициент замедления корабля
SHIP_DECELERATION_FACTOR = 150
# скорость настолько маленькая, что считающуюся 0
SHIP_MIN_VELOCITY = 0.1

# константы для астероидов
# размерности астероидов
BIG, MEDIUM, SMALL = 3, 2, 1
ASTEROID_SCALES = {BIG: 1.0,
                   MEDIUM: 0.5,
                   SMALL: 0.25}
ASTEROID_RADII = {BIG: 35,
                  MEDIUM: 35 / 2,
                  SMALL: 35 / 1.5}

MAX_ASTEROID_VELOCITY, MIN_ASTEROID_VELOCITY = 3, 1
# Радиус относительно корабля в котором не могут заспавнится астероиды
MIN_ASTEROID_DISTANCE = 400

# константы для пуль
BULLET_SPEED = 5

# константы для нло
UFO_SCORE = 4
UFO_RADIUS = 16
UFO_MIN_VELOCITY = 1
UFO_MAX_VELOCITY = 2
UFO_SHOOT_EVENT = pygame.USEREVENT + 1
SHIP_RECOVERY = pygame.USEREVENT + 2
BOOSTER_PICKUP = pygame.USEREVENT + 3
UFO_BULLET_SPEED = 3

SCORE = {BIG: 20,
         MEDIUM: 50,
         SMALL: 100,
         UFO_SCORE: 120}

EXIT_TABLE = 0
ENTER_NAME = 1
SHOW_TABLE = 2