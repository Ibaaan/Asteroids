# размеры экрана
from enum import Enum, auto

from pygame.event import custom_type


SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

FIELD_HEIGHT = 768
FIELD_WIDTH = 1024

# константы для корабля
SHIP_MAX_VELOCITY = 0.15
SHIP_ANGULAR_VELOCITY = 4
CLOCKWISE = 1
COUNTER_CLOCKWISE = 2
ACCELERATE = 3
AFTER_DEATH_DURATION = 10
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
UFO_UPDATE_EVENT = custom_type()
SHIP_RECOVERY_EVENT = custom_type()
BOOSTER_ENDED = custom_type()

SCORE = {BIG: 20,
         MEDIUM: 50,
         SMALL: 100,
         UFO_SCORE: 120}
# Game states
MAIN_MENU_STATE = 0
GAME_RUN_STATE = 1
GAME_OVER_STATE = 2
LEADERBOARD_STATE = 3
SAVE_RESULT_STATE = 4

# Events for changing game state
GAME_OVER_EVENT = custom_type()
GAME_RUN_EVENT = custom_type()
LEADERBOARD_EVENT = custom_type()
SAVE_RESULT_EVENT = custom_type()
BACK_FROM_LEADERBOARD_EVENT = custom_type()
SLIDER_DRAGGING_EVENT = custom_type()

NO_PIXEL = 0


class SpritesEnum(Enum):
    booster = auto()
    ship_stay = auto()
    nothing = auto()
    ship_move = auto()
    asteroid_b1 = auto()
    asteroid_b2 = auto()
    asteroid_b3 = auto()
    asteroid_m1 = auto()
    asteroid_m2 = auto()
    asteroid_m3 = auto()
    asteroid_s1 = auto()
    asteroid_s2 = auto()
    asteroid_s3 = auto()
    bullet = auto()
    ufo = auto()
    background = auto()
