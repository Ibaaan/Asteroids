import random
from copy import copy

import pygame
from PIL import Image, ImageStat, ImageFile
from pygame import Surface

from resources.constants import BIG, MEDIUM, SMALL, SpritesEnum
from resources.utils import load_sprite


def _surface_to_pilImage(surface: Surface):
    pil_string_image = pygame.image.tobytes(surface, 'RGBA')
    return Image.frombytes('RGBA', surface.size, pil_string_image)


def _give_pixelated(image: ImageFile, pixelation_amount):
    size = image.size
    og = image.resize(size)

    output = Image.new('RGBA', size)

    for i in range(0, size[0], pixelation_amount):
        for j in range(0, size[1], pixelation_amount):
            box = (i, j, i + pixelation_amount, j + pixelation_amount)
            region = og.crop(box)
            median = ImageStat.Stat(region).median
            r = Image.new('RGBA', (pixelation_amount, pixelation_amount), tuple(median))
            output.paste(r, (i, j))

    return output


def _pilImage_to_surface(pilImage):
    return (pygame.image.frombytes(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha())


def _pixelate_image(sprite, pixel_rate):
    """
    :param sprite: спрайт
    """
    pilImage = _surface_to_pilImage(sprite)
    pil_sprite = _give_pixelated(pilImage, pixel_rate)
    return _pilImage_to_surface(pil_sprite)


class SpritesManager:
    raw_sprites: dict[SpritesEnum, Surface] = {}
    pixel_sprites: dict[SpritesEnum, Surface] = {}

    @classmethod
    def init_default_sprites(cls):
        cls.raw_sprites[SpritesEnum.ship_stay] = load_sprite("ship_stay")
        cls.raw_sprites[SpritesEnum.nothing] = load_sprite("nothing")
        cls.raw_sprites[SpritesEnum.ship_move] = load_sprite("ship_move")
        cls.raw_sprites[SpritesEnum.asteroid_b1] = load_sprite("big_rock1")
        cls.raw_sprites[SpritesEnum.asteroid_b2] = load_sprite("big_rock2")
        cls.raw_sprites[SpritesEnum.asteroid_b3] = load_sprite("big_rock3")
        cls.raw_sprites[SpritesEnum.asteroid_m1] = load_sprite("medium_rock1")
        cls.raw_sprites[SpritesEnum.asteroid_m2] = load_sprite("medium_rock2")
        cls.raw_sprites[SpritesEnum.asteroid_m3] = load_sprite("medium_rock3")
        cls.raw_sprites[SpritesEnum.asteroid_s1] = load_sprite("small_rock1")
        cls.raw_sprites[SpritesEnum.asteroid_s2] = load_sprite("small_rock2")
        cls.raw_sprites[SpritesEnum.asteroid_s3] = load_sprite("small_rock3")
        cls.raw_sprites[SpritesEnum.bullet] = load_sprite("bullet")
        cls.raw_sprites[SpritesEnum.ufo] = load_sprite("ufo")
        cls.raw_sprites[SpritesEnum.booster] = pygame.Surface((2 * 9, 2 * 9), pygame.SRCALPHA)

        cls.pixel_sprites = copy(cls.raw_sprites)

    @classmethod
    def asteroid_sprite(cls, size_name: int):
        number = random.randint(0, 2)
        sprite_name = cls._get_asteroid_sprites().get(size_name)[number]
        return cls.get_sprite(sprite_name), sprite_name

    @classmethod
    def _get_asteroid_sprites(cls):
        return {
            BIG: [SpritesEnum.asteroid_b1,
                  SpritesEnum.asteroid_b2,
                  SpritesEnum.asteroid_b3],
            MEDIUM: [SpritesEnum.asteroid_m1,
                     SpritesEnum.asteroid_m2,
                     SpritesEnum.asteroid_m3],
            SMALL: [SpritesEnum.asteroid_s1,
                    SpritesEnum.asteroid_s2,
                    SpritesEnum.asteroid_s3]
        }

    @classmethod
    def get_sprite(cls, sprite: SpritesEnum):
        return cls.pixel_sprites[sprite]

    @classmethod
    def pixelate_sprites(cls, pixel_rate):
        if pixel_rate == -1:
            cls.pixel_sprites = copy(cls.raw_sprites)
        else:
            for name, sprite in cls.raw_sprites.items():
                cls.pixel_sprites[name] = _pixelate_image(sprite, pixel_rate)

    @classmethod
    def get_raw_sprite(cls, sprite):
        return cls.raw_sprites[sprite]