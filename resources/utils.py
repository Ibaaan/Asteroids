import os
import random

from pygame.image import load
from pygame.math import Vector2

from resources.settings import WIDTH, HEIGHT


def wrap_position(old_position: Vector2):
    """
    Делает из игрового поля тор
    :param old_position: Старые координаты
    :return: Новые координаты, такие что, если old_position находится вне
        игрового поля, то новые будут на противоположной стороне
    """
    return Vector2(old_position.x % WIDTH, old_position.y % HEIGHT)


def get_random_vel_dir(min_speed, max_speed):
    """
    :param min_speed: минимальная скорость
    :param max_speed:  максимальная скорость
    :return: Случайную величину скорости от min_speed до max_speed
        с шагом 0.1; единичный вектор скорости
    """
    speed = random.randint(min_speed * 10, max_speed * 10) / 10
    angle = random.randrange(0, 360)
    return speed, Vector2(1, 0).rotate(angle)


def load_sprite(name):
    """
    :param name: Имя спрайта для загрузки
    :return: спрайт с соответствующим именем
    """
    path = os.path.join("resources", "sprites", f"{name}.png")
    loaded_sprite = load(path)
    return loaded_sprite


def sprite_for_asteroid(size_name):
    """
    :param size_name: Константа размера астероида
    :return: спрайт для астероида в зависимости от его размера
    """
    number = random.randint(1, 3)
    if size_name == 3:
        name = 'big_rock'
    elif size_name == 2:
        name = 'medium_rock'
    else:
        name = 'small_rock'
    return load_sprite(name + str(number))


def get_random_position():
    """
    :return: Случайную координату на игровом поле
    """
    return Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))


def randomize_vector_direction(vector: Vector2):
    """
    :return: единичный вектор отличающийся от данного
        максимум на 15 градусов
    """
    vector.normalize_ip()
    angle_to_rotate = random.randint(-15, 15)
    return vector.rotate(angle_to_rotate)
