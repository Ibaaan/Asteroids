import pygame
from pygame.time import set_timer

from resources.settings import (COUNTER_CLOCKWISE,
                                CLOCKWISE,
                                UFO_SHOOT_EVENT,
                                SCORE,
                                MIN_ASTEROID_DISTANCE,
                                BIG, UFO_SCORE, SHIP_RECOVERY)
from resources.utils import get_random_position, load_sprite
from src.GameObjects import GameObject, Asteroid, Ship, UFO


class Model:
    def __init__(self):
        self.lives = 5
        self.ufos = []
        self.asteroids = []
        self.ship_bullets = []
        self.ufo_bullets = []
        self.ship = Ship(self.ship_bullets.append)
        self.score = 0
        self.run = True
        self.level = 1
        self._init_game_objects()

        set_timer(UFO_SHOOT_EVENT, 1500)


    def tick(self):
        self._controller()
        if self.run:
            self._model()

    def _controller(self):
        """
        Просчитывает инпуты
        """
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.ship.shoot()
                if e.key == pygame.K_r:
                    self._reset_variables()
                    self._init_game_objects()
            elif e.type == UFO_SHOOT_EVENT:
                if not self.ufos:
                    continue
                for ufo in self.ufos:
                    ufo.shoot_at(self.ship.position)
                    ufo.change_velocity()
            elif e.type == SHIP_RECOVERY:
                self.ship.change_sprites()


        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_d]:
            self.ship.rotate(CLOCKWISE)
        if is_key_pressed[pygame.K_a]:
            self.ship.rotate(COUNTER_CLOCKWISE)
        if is_key_pressed[pygame.K_w]:
            self.ship.accelerate()

    def _model(self):
        """
        Просчитывает мо
        """
        self._calc_collisions()
        self._move_objects()
        self.ship.decrease_velocity()

        if not self.asteroids:
            self.level += 1
            self._init_game_objects()

    def _calc_collisions(self):
        """
        Считает коллизии всех игровых объектов
        """
        for object in [*self.asteroids, *self.ufo_bullets, *self.ufos]:
            if object.collides_with(self.ship):
                self.lives -= 1
                self.ship.position = self.new_ship_pos()
                set_timer(SHIP_RECOVERY, 90, 10)
                if self.lives == 0:
                    self.run = False


        for bullet in self.ship_bullets:
            for asteroid in self.asteroids:
                if asteroid.collides_with(bullet):
                    self.score += SCORE[asteroid.size_name]
                    self.asteroids.remove(asteroid)
                    try:
                        self.ship_bullets.remove(bullet)
                    except ValueError as e:
                        print(e)

                    asteroid.split()

        for bullet in self.ship_bullets:
            for ufo in self.ufos:
                if ufo.collides_with(bullet):
                    self.score += SCORE[UFO_SCORE]
                    self.ufos.remove(ufo)
                    try:
                        self.ship_bullets.remove(bullet)
                    except ValueError as e:
                        print(e)

        if len(self.ship_bullets) > 4:
            self.ship_bullets.pop(0)

    def _move_objects(self):
        """
        Двигает все объекты на поле
        """
        for game_object in self.get_game_objects():
            game_object.move()

    def get_game_objects(self) -> list[GameObject]:
        """
        :return: Список всех игровых объектов,
            как список GameObject объектов
        """
        game_objects = [*self.asteroids, *self.ship_bullets, self.ship,
                        *self.ufos, *self.ufo_bullets]
        return game_objects

    def _init_game_objects(self):
        """
        Инициализация начального состояния игры
        """
        self._create_asteroids(self.level)
        self._create_ufos(self.level)

    def _create_asteroids(self, level):
        """
        Добавляет некоторое количество астероидов в зависимости от уровня
        :param level: уровень
        """
        for _ in range(2 + level):
            while True:
                position = get_random_position()
                if (
                        position.distance_to(self.ship.position)
                        > MIN_ASTEROID_DISTANCE
                ):
                    break
            self.asteroids.append(Asteroid(BIG, position,
                                           self.asteroids.append))

    def _create_ufos(self, level):
        for i in range(level):
            while True:
                position = get_random_position()
                if (
                        position.distance_to(self.ship.position)
                        > MIN_ASTEROID_DISTANCE
                ):
                    break
            new_ufo = UFO(position, self.ufo_bullets.append)
            self.ufos.append(new_ufo)

    def _reset_variables(self):
        self.ufos = []
        self.asteroids = []
        self.ship_bullets = []
        self.ufo_bullets = []
        self.ship = Ship(self.ship_bullets.append)
        self.score = 0
        self.run = True
        self.level = 1
        self.lives = 5

    def new_ship_pos(self):
        while True:
            pos = get_random_position()
            for object in [*self.asteroids,*self.ufos, *self.ufo_bullets]:
                if pos.distance_to(object.position) < 100:
                    continue
            return pos