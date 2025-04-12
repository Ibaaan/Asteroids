import pygame
from pygame.math import Vector2

from resources.settings import (WIDTH,
                                HEIGHT,
                                SHIP_ANGULAR_VELOCITY,
                                SHIP_MAX_VELOCITY,
                                ACCELERATION_FACTOR,
                                SHIP_MIN_VELOCITY, ASTEROID_RADII,
                                MIN_ASTEROID_VELOCITY, MAX_ASTEROID_VELOCITY, UFO_RADIUS, UFO_MIN_VELOCITY,
                                UFO_MAX_VELOCITY, UFO_BULLET_SPEED)
from resources.utils import (wrap_position,
                             get_random_velocity,
                             load_sprite,
                             sprite_for_asteroid, randomize_vector_direction)


class GameObject:
    """
    Общий предок для всех объектов в игре
    """

    def __init__(self, velocity: Vector2,
                 position: Vector2, sprite, radius):
        """
        Конструктор игрового объект
        :param velocity: Скорость игрового объект
        :param position: Координаты игрового объект
        :param sprite: Спрайт для отрисовки игрового объект
        :param radius: Радиус окружности,
            представляющей хит бокс игрового объект
        """
        self.position = position
        self.velocity = velocity
        self.sprite = sprite
        self.radius = radius

    def move(self):
        """
        Перемещает игровой объект
        """
        new_position = self.position + self.velocity
        self.position = wrap_position(new_position)

    def draw(self, screen):
        """
        Отрисовка игрового объекта на экране
        :param screen: экран
        """
        blit_position = self.position - Vector2(self.radius)
        screen.blit(self.sprite, blit_position)

    def collides_with(self, game_object):
        """
        Проверяет колизится ли этот объект с данным
        :param game_object: данный игровой объект
        :return: True - если хит боксы пересекаются,
            False - иначе
        """
        distance = self.position.distance_to(game_object.position)
        return distance < self.radius + game_object.radius


class Ship(GameObject):
    """
    Класс корабля
    """
    ship_stay_sprite = load_sprite("ship_stay")
    ship_move_sprite = load_sprite("ship_move")
    nothing_sprite = load_sprite("nothing")

    def __init__(self, add_bullet):
        """
        Конструктор корабля
        :param add_bullet: callback на добавление пуль
        """
        # last_direction - направление инерции корабля
        self.direction = Vector2(0, -1)
        self.add_bullet = add_bullet
        self.afterdeath_sprite_flag = False
        self.ship_move_flag = False
        super().__init__(velocity=Vector2(0, 0),
                         position=Vector2(WIDTH / 2, HEIGHT / 2),
                         sprite=self.ship_stay_sprite,
                         radius=10)

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

    def shoot(self, speed):
        """
        Корабль стреляет в перед собой
        """
        bullet = Bullet(self.position, speed, self.direction)
        self.add_bullet(bullet)

    def draw(self, screen):
        """
        Отрисовка корабля на экране
        :param screen: экран
        """
        angle = self.direction.angle_to(Vector2(0, -1))
        ship = pygame.transform.rotate(self.sprite, angle + 90)
        ship_rect = ship.get_rect(center=self.position)
        screen.blit(ship, ship_rect)

        self._change_sprite()

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
        :return:
        """
        self.afterdeath_sprite_flag = True

    def _change_sprite(self):
        """
        Меняет спрайт для анимации движения и при смерти
        """
        if self.afterdeath_sprite_flag and self.sprite != self.nothing_sprite:
            self.afterdeath_sprite_flag = False
            self.sprite = self.nothing_sprite
            return

        if self.ship_move_flag and self.sprite != self.ship_move_sprite:
            self.ship_move_flag = False
            self.sprite = self.ship_move_sprite
            return

        if self.sprite != self.ship_stay_sprite:
            self.sprite = self.ship_stay_sprite


class Asteroid(GameObject):
    """
    Класс астероида
    """

    def __init__(self, size_name, position, add_asteroid):
        """
        Конструктор астероида
        :param size_name: константа представляющая размер астероида,
            смотри settings.py
        :param position: Первоначальная позиция астероида
        :param add_asteroid: callback на добавление новых астероидов
        """
        self.add_asteroid = add_asteroid
        self.size_name = size_name
        velocity = get_random_velocity(MIN_ASTEROID_VELOCITY,
                                       MAX_ASTEROID_VELOCITY)

        super().__init__(velocity=velocity,
                         position=position,
                         sprite=sprite_for_asteroid(size_name),
                         radius=ASTEROID_RADII.get(size_name))

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
                         sprite=load_sprite('bullet'),
                         radius=3)

    def move(self):
        """
        Перемещает пулю
        """
        self.position = self.position + self.velocity


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
                         sprite=load_sprite('ufo'),
                         radius=UFO_RADIUS)

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


class Booster(GameObject):
    """
    Класс бустера увеличивающего скорость полета пуль корабля
    """

    def __init__(self, position):
        # Зеленый круг радиуса 9
        surface = pygame.Surface((2 * 9, 2 * 9), pygame.SRCALPHA)
        super().__init__(velocity=Vector2(0, 0),
                         position=position,
                         sprite=surface,
                         radius=9)
        pygame.draw.circle(surface, 'green', (9, 9), 9)

    def draw(self, screen):
        screen.blit(self.sprite, self.position)
