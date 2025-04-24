import pygame
from pygame import Vector2
from pygame.sprite import Group, Sprite
from pygame.time import set_timer

from resources.SpritesManager import SpritesManager
from resources.constants import (COUNTER_CLOCKWISE,
                                 CLOCKWISE,
                                 UFO_UPDATE_EVENT,
                                 MIN_ASTEROID_DISTANCE,
                                 BIG, ACCELERATE,
                                 GAME_RUN_STATE, SHIP_RECOVERY_EVENT, GAME_OVER_EVENT, SCORE, UFO_SCORE, BOOSTER_ENDED,
                                 AFTER_DEATH_DURATION, SCREEN_WIDTH, SCREEN_HEIGHT, FIELD_WIDTH,
                                 FIELD_HEIGHT)
from resources.utils import get_random_position
from src.GameObjects import GameObject, Asteroid, Ship, UFO, Booster


class GameModel:
    """
    Модель со всей логикой игры
    """

    lives: int
    ufos: Group
    asteroids: Group
    ship_bullets: Group
    ufo_bullets: Group
    ship: Ship
    score: int
    level: int
    boosters: Group
    is_after_death = False

    def __init__(self):
        self.ship = None

        set_timer(UFO_UPDATE_EVENT, 1500)

    def reset_variables(self):
        """
        Возвращает все переменные в исходное состояние
        """
        self.lives = 5
        self.ufos = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.ship_bullets = pygame.sprite.Group()
        self.ufo_bullets = pygame.sprite.Group()
        self.ship = Ship(self.ship_bullets.add)
        self.score = 0
        self.level = 1
        self.boosters = pygame.sprite.Group()

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
            self.init_game_objects()
        self.is_after_death = False

    def _calc_collisions(self):
        """
        Считает коллизии всех игровых объектов
        """

        if (
                # Коллизия корабля с вражескими объектами
                (self.ship.collides_with(self.asteroids, False) or
                 self.ship.collides_with(self.ufo_bullets, False) or
                 self.ship.collides_with(self.ufos, False)) and
                not self.is_after_death
        ):
            self.lives -= 1
            self.ship.position = self.new_ship_pos()
            set_timer(SHIP_RECOVERY_EVENT, 90, AFTER_DEATH_DURATION)
            if self.lives <= 0:
                pygame.event.post(pygame.event.Event(GAME_OVER_EVENT))

        # Коллизия пуль корабля
        for bullet in self.ship_bullets:
            # Коллизия пуль корабля с астероидами
            collides_with = bullet.collides_with(self.asteroids, True)
            for sprite in collides_with:
                self.score += SCORE[sprite.size_name]
                self.ship_bullets.remove(bullet)
                sprite.split()

            # Коллизия пуль корабля с нло
            if bullet.collides_with(self.ufos, True):
                self.score += SCORE[UFO_SCORE]
                self.ship_bullets.remove(bullet)

        # Коллизия корабля c бустером
        ship_collides_with = self.ship.collides_with(self.boosters, True)
        if ship_collides_with:
            self.ship.change_bullet_speed(True)
            set_timer(BOOSTER_ENDED, 10000, 1)

        # Проверка, что пуль не больше 4
        if len(self.ship_bullets) > 4:
            distance_to = 0
            bullet_to_remove = None
            for bullet in self.ship_bullets:
                if bullet.position.distance_to(self.ship.position) > distance_to:
                    bullet_to_remove = bullet
                    distance_to = bullet.position.distance_to(self.ship.position)
            try:
                self.ship_bullets.remove(bullet_to_remove)
            finally:
                pass

        if len(self.ufo_bullets) > 4:
            distance_to = 0
            bullet_to_remove = None
            for bullet in self.ufo_bullets:
                if bullet.position.distance_to(self.ship.position) > distance_to:
                    bullet_to_remove = bullet
                    distance_to = bullet.position.distance_to(self.ship.position)
            try:
                self.ufo_bullets.remove(bullet_to_remove)
            finally:
                pass

    def _move_objects(self):
        """
        Двигает все объекты на поле
        """
        for game_object in self.get_all_game_objects():
            game_object.move()

    def get_camera_group(self):
        return GameView(*self.asteroids, *self.ship_bullets,
                        *self.ufos, *self.ufo_bullets, *self.boosters)

    def get_all_game_objects(self) -> list[GameObject]:
        """
        :return: Список всех игровых объектов, как список GameObject объектов
        """
        game_objects = [*self.asteroids, *self.ship_bullets, self.ship,
                        *self.ufos, *self.ufo_bullets, *self.boosters]
        return game_objects

    def init_game_objects(self):
        """
        Инициализация начального состояния игры
        """
        self._create_asteroids(self.level)
        self._create_ufos(self.level)
        self.boosters.add(Booster(get_random_position()))

    def _create_asteroids(self, level):
        """
        Добавляет некоторое количество астероидов в зависимости от уровня
        :param level: уровень
        """
        for _ in range(4 + level):
            while True:
                position = get_random_position()
                if (
                        position.distance_to(self.ship.position)
                        > MIN_ASTEROID_DISTANCE
                ):
                    break
            asteroid = Asteroid(BIG, position, self.asteroids.add)
            self.asteroids.add(asteroid)

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
            new_ufo = UFO(position, self.ufo_bullets.add)
            self.ufos.add(new_ufo)

    def ship_shoot(self):
        self.ship.shoot()

    def new_ship_pos(self):
        """
        Новая позиция корабля после столкновения
        :return:
        """
        while True:
            pos = get_random_position()
            for game_object in [*self.asteroids, *self.ufos, *self.ufo_bullets]:
                if pos.distance_to(game_object.position) < 100:
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


class GameView(pygame.sprite.Group):
    half_w = SCREEN_WIDTH // 2
    half_h = SCREEN_HEIGHT // 2

    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.display_surface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()

    def custom_draw(self, player: Sprite):
        self._center_target_camera(player)

        self._draw_background()

        for sprite in self.sprites():
            self._draw(sprite)

        self.display_surface.blit(player.image, player.rect.topleft - self.offset)

    def _center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def _draw(self, sprite: Sprite):
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                offset_pos = (sprite.rect.topleft - self.offset
                              + Vector2(x * FIELD_WIDTH, y * FIELD_HEIGHT))
                self.display_surface.blit(sprite.image, offset_pos)

    def _draw_background(self):
        self._draw(SpritesManager.get_background_sprite())
