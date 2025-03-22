import os
import random

from pygame.image import load
from pygame.math import Vector2

from asteroids.resources.settings import WIDTH, HEIGHT


def wrap_position(new_position: Vector2):
    return Vector2(new_position.x % WIDTH, new_position.y % HEIGHT)


def get_random_vel_dir(min_speed, max_speed):
    speed = random.randint(min_speed * 10, max_speed * 10) / 10
    angle = random.randrange(0, 360)
    return speed, Vector2(1, 0).rotate(angle)


def load_sprite(name):
    path = os.path.join("resources", "sprites", f"{name}.png")
    loaded_sprite = load(path)
    return loaded_sprite


def sprite_for_asteroid(size_name):
    number = random.randint(1, 3)
    if size_name == 3:
        name = 'big_rock'
    elif size_name == 2:
        name = 'medium_rock'
    else:
        name = 'small_rock'
    return load_sprite(name + str(number))


def get_random_position():
    return Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
