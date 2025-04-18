import pygame
from pygame.time import set_timer

from resources.settings import (COUNTER_CLOCKWISE,
                                CLOCKWISE,
                                UFO_UPDATE_EVENT,
                                SCORE,
                                MIN_ASTEROID_DISTANCE,
                                BIG, UFO_SCORE, SHIP_RECOVERY_EVENT, BOOSTER_ENDED, ACCELERATE,
                                GAME_OVER_EVENT, GAME_RUN_STATE)
from resources.utils import get_random_position
from src.GameObjects import GameObject, Asteroid, Ship, UFO, Booster


class GameModel:
    """
    Модель со всей логикой игры
    """

    lives: int
    ufos:list
    asteroids:list
    ship_bullets:list
    ufo_bullets:list
    ship:Ship
    score:int
    level:int
    boosters:list

    def __init__(self):
        self.reset_variables()
        self._init_game_objects()
        set_timer(UFO_UPDATE_EVENT, 1500)

    def reset_variables(self):
        """
        Возвращает все переменные в исходное состояние
        """
        self.lives = 0
        self.ufos = []
        self.asteroids = []
        self.ship_bullets = []
        self.ufo_bullets = []
        self.ship = Ship(self.ship_bullets.append)
        self.score = 0
        self.level = 1
        self.boosters = []

    def update(self, game_state):
        """
        Обновляет модель, если игра идет
        :param game_state: Отвечает за то, идет ли игра
        """
        if game_state != GAME_RUN_STATE:
            return

        self._calc_collisions()
        self._move_objects()

        if not self.asteroids:
            self.level += 1
            self._init_game_objects()

    def _calc_collisions(self):
        """
        Считает коллизии всех игровых объектов
        """
        for game_object in [*self.asteroids, *self.ufo_bullets, *self.ufos]:
            if game_object.collides_with(self.ship):
                self.lives -= 1
                self.ship.position = self.new_ship_pos()
                set_timer(SHIP_RECOVERY_EVENT, 90, 10)
                if self.lives <= 0:
                    pygame.event.post(pygame.event.Event(GAME_OVER_EVENT))

        for bullet in self.ship_bullets:
            for asteroid in self.asteroids:
                if asteroid.collides_with(bullet):
                    self.score += SCORE[asteroid.size_name]
                    self.asteroids.remove(asteroid)
                    try:
                        self.ship_bullets.remove(bullet)
                    except ValueError:
                        pass
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

        for booster in self.boosters:
            if self.ship.collides_with(booster):
                self.ship.change_bullet_speed(True)
                set_timer(BOOSTER_ENDED, 10000, 1)
                self.boosters.remove(booster)

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
                        *self.ufos, *self.ufo_bullets, *self.boosters]
        return game_objects

    def _init_game_objects(self):
        """
        Инициализация начального состояния игры
        """
        self._create_asteroids(self.level)
        self._create_ufos(self.level)
        self.boosters.append(Booster(get_random_position()))

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
        """
        Создает несколько нло
        :param level: То сколько нло будет создано
        """
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

    def ship_shoot(self):
        self.ship.shoot()

    def new_ship_pos(self):
        """
        Новая позиция корабля после столкновения
        :return:
        """
        while True:
            pos = get_random_position()
            for object in [*self.asteroids, *self.ufos, *self.ufo_bullets]:
                if pos.distance_to(object.position) < 100:
                    continue
            return pos

    def on_ufo_update(self):
        for ufo in self.ufos:
            ufo.shoot_at(self.ship.position)
            ufo.change_velocity()

    def after_death_animation(self):
        self.ship.after_death_animation()

    def booster_ended(self):
        self.ship.change_bullet_speed(False)

    def on_ship_input(self, action_id):
        """
        Выполняет действия изменяя параметры корабля
        """
        if action_id == CLOCKWISE:
            self.ship.rotate(True)
        elif action_id == COUNTER_CLOCKWISE:
            self.ship.rotate(False)
        elif action_id == ACCELERATE:
            self.ship.accelerate()
