from pygame.color import THECOLORS

HEIGHT = 600
WIDTH = 800

COLOR = THECOLORS.get("aliceblue")

MAX_VELOCITY = 2.7
ANGULAR_VELOCITY = 4
CLOCKWISE = True
COUNTER_CLOCKWISE = False

# Чем больше, тем дольше будет корабль лететь по инерции
DECELERATION_FACTOR = 150
DBL_EPSILON = 0.1
BIG, MEDIUM, SMALL = 3, 2, 1
ASTEROID_SCALES = {BIG: 1.0,
                   MEDIUM: 0.5,
                   SMALL: 0.25}
ASTEROID_RADIUSES = {BIG: 35,
                   MEDIUM: 35/2,
                   SMALL: 35/1.5}
ASTEROIDS_SCORE = {BIG: 20,
                   MEDIUM: 50,
                   SMALL: 100}
MAX_ASTEROID_V, MIN_ASTEROID_V = 3, 1
BULLET_SPEED = 5
MIN_ASTEROID_DISTANCE = 400
