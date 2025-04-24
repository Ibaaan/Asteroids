import pygame
from pygame import Surface
from pygame.math import Vector2

from resources import SpritesManager
from resources.SpritesManager import SpritesManager
from resources.constants import (FIELD_WIDTH,
                                 FIELD_HEIGHT,
                                 SHIP_ANGULAR_VELOCITY,
                                 SHIP_MAX_VELOCITY,
                                 ACCELERATION_FACTOR,
                                 SHIP_MIN_VELOCITY, MIN_ASTEROID_VELOCITY, MAX_ASTEROID_VELOCITY, UFO_MIN_VELOCITY,
                                 UFO_MAX_VELOCITY, UFO_BULLET_SPEED, BULLET_SPEED, SpritesEnum)
from resources.utils import (wrap_position,
                             get_random_velocity,
                             randomize_vector_direction)


class GameObject(pygame.sprite.Sprite):
    """
    Общий предок для всех объектов в игре
    """

    def __init__(self, velocity: Vector2,
                 position: Vector2, image: Surface, sprite_id: SpritesEnum):
        """
        Конструктор игрового объект
        :param velocity: Скорость игрового объект
        :param position: Координаты игрового объект
        :param image: Спрайт для отрисовки игрового объект
        :param sprite_id: Радиус окружности,
            представляющей хит бокс игрового объект
        """

        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.velocity = velocity
        self.image = image
        self.name = sprite_id

        self._update_mask()

    def move(self):
        """
        Перемещает игровой объект
        """
        new_position = self.position + self.velocity
        self.position = wrap_position(new_position)

    def collides_with(self, game_object_group, doKill):
        """
        Проверяет колизится ли этот объект с данной группой
        :param game_object_group: данной группой объектов
        :return: True - если хит боксы пересекаются,
            False - иначе
        """
        if len(game_object_group) == 0:
            return list()
        if pygame.sprite.spritecollide(self, game_object_group, False):
            return pygame.sprite.spritecollide(self, game_object_group, doKill,
                                               pygame.sprite.collide_mask)
        else:
            return list()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._update_mask()

    def _update_mask(self):
        image = SpritesManager.get_raw_sprite(self.name)
        self.rect = image.get_rect()
        self.rect.center = self.position
        self.mask = pygame.mask.from_surface(image)


class Ship(GameObject):
    """
    Класс корабля
    """

    bullet_speed = BULLET_SPEED
    _nothing: Surface
    _ship_move: Surface
    _ship_stay: Surface

    def __init__(self, add_bullet):
        """
        Конструктор корабля
        :param add_bullet: callback на добавление пуль
        """

        self._nothing = SpritesManager.get_sprite(SpritesEnum.nothing)

        self.direction = Vector2(0, -1)
        self.add_bullet = add_bullet
        self.afterdeath_sprite_flag = False
        self.ship_move_flag = False
        self._ship_move = SpritesManager.get_sprite(SpritesEnum.ship_move)
        self._ship_stay = SpritesManager.get_sprite(SpritesEnum.ship_stay)
        super().__init__(velocity=Vector2(0, 0),
                         position=Vector2(FIELD_WIDTH / 2, FIELD_HEIGHT / 2),
                         image=self._ship_stay,
                         sprite_id=SpritesEnum.ship_stay)

    def rotate(self, clockwise):
        """
        Поворачивает корабль
        :param clockwise: если true -> вращать по часовой стрелке;
            в противном случае вращать против часовой стрелки
        """
        sign = 1 if clockwise else -1
        self.direction.rotate_ip(SHIP_ANGULAR_VELOCITY * sign)

    def accelerate(self):
        """
        Ускоряет корабль до максимальной скорости
        """
        self.velocity += SHIP_MAX_VELOCITY * self.direction
        self.ship_move_flag = True

    def shoot(self):
        """
        Корабль стреляет в перед собой
        """
        bullet = Bullet(self.position, self.bullet_speed, self.direction)
        self.add_bullet(bullet)

    def update(self, *args, **kwargs):
        self._change_image()
        angle = self.direction.angle_to(Vector2(0, -1))
        self.image = pygame.transform.rotate(self.image, angle + 90)
        super().update(*args, **kwargs)

    def _update_mask(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        """
        Перемещает корабль
        """
        new_position = self.position + self.velocity
        self.position = wrap_position(new_position)
        self.velocity *= ACCELERATION_FACTOR
        if self.velocity.length() - SHIP_MIN_VELOCITY < 0:
            self.velocity = Vector2(0, 0)

    def after_death_animation(self):
        """
        Проигрывают анимацию при потере жизни
        """
        self.afterdeath_sprite_flag = True

    def _change_image(self):
        """
        Меняет спрайт для анимации движения и при смерти
        """
        if self.afterdeath_sprite_flag:
            self.afterdeath_sprite_flag = False
            self.image = self._nothing
            return

        if self.ship_move_flag:
            self.ship_move_flag = False
            self.image = self._ship_move
            return
        self.image = self._ship_stay

    def change_bullet_speed(self, is_boost):
        """
        Изменения пули
        """
        if is_boost:
            self.bullet_speed = BULLET_SPEED * 3
        else:
            self.bullet_speed = BULLET_SPEED


class Asteroid(GameObject):
    """
    Класс астероида
    """

    def __init__(self, size_name, position, add_asteroid):
        """
        Конструктор астероида
        :param size_name: константа представляющая размер астероида,
            смотри constants.py
        :param position: Первоначальная позиция астероида
        :param add_asteroid: callback на добавление новых астероидов
        """
        self.add_asteroid = add_asteroid
        self.size_name = size_name
        velocity = get_random_velocity(MIN_ASTEROID_VELOCITY,
                                       MAX_ASTEROID_VELOCITY)

        sprite, sprite_name = SpritesManager.asteroid_sprite(size_name)
        super().__init__(velocity=velocity,
                         position=position,
                         image=sprite,
                         sprite_id=sprite_name)

    def split(self):
        """
        Разбивает астероид на несколько более маленьких
        (астероид надо удалить)
        """
        if self.size_name > 1:
            for _ in range(2):
                new_asteroid = Asteroid(self.size_name - 1, self.position,
                                        self.add_asteroid)
                self.add_asteroid(new_asteroid)


class Bullet(GameObject):
    """
    Класс пули
    """

    def __init__(self, position, speed, direction):
        """
        Конструктор
        :param position: Первоначальная позиция пули
        :param speed: Скорость пули
        :param direction: Направление движения пули
        """
        super().__init__(velocity=speed * direction.copy(),
                         position=position,
                         image=SpritesManager.get_sprite(SpritesEnum.bullet),
                         sprite_id=SpritesEnum.bullet)


class UFO(GameObject):
    """
    Класс нло, штука стреляет в игрока
    """

    def __init__(self, position, add_bullets):
        self.add_bullets = add_bullets
        velocity = get_random_velocity(UFO_MIN_VELOCITY,
                                       UFO_MAX_VELOCITY)
        super().__init__(velocity=velocity,
                         position=position,
                         image=SpritesManager.get_sprite(SpritesEnum.ufo),
                         sprite_id=SpritesEnum.ufo)

    def shoot_at(self, ship_position: Vector2):
        """
        Создает пулю в направлении корабля с некоторым разбросом
        :param ship_position: координаты корабля
        :return:
        """
        vector_to_ship = ship_position - self.position
        new_bullet = Bullet(self.position, UFO_BULLET_SPEED,
                            randomize_vector_direction(vector_to_ship))
        self.add_bullets(new_bullet)

    def change_velocity(self):
        """
        Изменяет скорость и направление
        """
        self.velocity = get_random_velocity(UFO_MIN_VELOCITY,
                                            UFO_MAX_VELOCITY)

    # def update_image(self, pixel_rate):
    #     self.image = Images.pixelate_image(Images.ufo, pixel_rate)


class Booster(GameObject):
    """
    Класс бустера увеличивающего скорость полета пуль корабля
    """

    def __init__(self, position):
        # Зеленый круг радиуса 9
        self.surface = pygame.Surface((2 * 9, 2 * 9), pygame.SRCALPHA)
        super().__init__(velocity=Vector2(0, 0),
                         position=position,
                         image=SpritesManager.get_sprite(SpritesEnum.booster),
                         sprite_id=SpritesEnum.booster)
        # pygame.draw.circle(surface, 'green', (9, 9), 9)

    def draw(self, screen):
        screen.blit(self.image, self.position)

    # def update_image(self, pixel_rate):
    #     self.image = Images.pixelate_image(self.surface, pixel_rate)
    #
