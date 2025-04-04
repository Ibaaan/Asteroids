# размеры экрана
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
ASTEROIDS_SCORE = {BIG: 20,
                   MEDIUM: 50,
                   SMALL: 100}
MAX_ASTEROID_VELOCITY, MIN_ASTEROID_VELOCITY = 3, 1
# Радиус относительно корабля в котором не могут заспавнится астероиды
MIN_ASTEROID_DISTANCE = 400

# константы для пуль
BULLET_SPEED = 5
