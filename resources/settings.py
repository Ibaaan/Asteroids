# размеры экрана
import pygame

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

FIELD_HEIGHT = 600
FIELD_WIDTH = 800

# константы для корабля
SHIP_MAX_VELOCITY = 0.2
SHIP_ANGULAR_VELOCITY = 4
CLOCKWISE = 1
COUNTER_CLOCKWISE = 2
ACCELERATE = 3
# коэффициент замедления корабля
ACCELERATION_FACTOR = 0.99
# скорость настолько маленькая, что считающуюся 0
SHIP_MIN_VELOCITY = 0.01

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
UFO_BULLET_SPEED = 3
# Events
UFO_UPDATE_EVENT = pygame.USEREVENT + 1
SHIP_RECOVERY_EVENT = pygame.USEREVENT + 2
BOOSTER_ENDED = pygame.USEREVENT + 3


SCORE = {BIG: 20,
         MEDIUM: 50,
         SMALL: 100,
         UFO_SCORE: 120}
# Game states
MAIN_MENU_STATE = 0
GAME_RUN_STATE = 1
GAME_OVER_STATE = 2
LEADERBOARD_STATE = 3

# Events for changing game state
GAME_OVER_EVENT = pygame.event.Event(pygame.USEREVENT + 4)
GAME_RUN_EVENT = pygame.event.Event(pygame.USEREVENT + 5)
LEADERBOARD_EVENT = pygame.event.Event(pygame.USEREVENT + 6)