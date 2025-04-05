import pygame
from pygame.math import Vector2

from resources.settings import (WIDTH,
                                HEIGHT,
                                SHIP_ANGULAR_VELOCITY,
                                SHIP_MAX_VELOCITY,
                                BULLET_SPEED,
                                SHIP_DECELERATION_FACTOR,
                                SHIP_MIN_VELOCITY, ASTEROID_RADII,
                                MIN_ASTEROID_VELOCITY, MAX_ASTEROID_VELOCITY, UFO_RADIUS, UFO_MIN_VELOCITY,
                                UFO_MAX_VELOCITY)
from resources.utils import (wrap_position,
                             get_random_vel_dir,
                             load_sprite,
                             sprite_for_asteroid, randomize_vector_direction)


class GameObject:
    """
    Общий предок для всех объектов в игре
    """

    def __init__(self, velocity: float, direction: Vector2,
                 position: Vector2, sprite, radius):
        """
        Конструктор игрового объект
        :param velocity: Скорость игрового объект
        :param direction: Направление игрового объект
        :param position: Координаты игрового объект
        :param sprite: Спрайт для отрисовки игрового объект
        :param radius: Радиус окружности,
            представляющей хит бокс игрового объект
        """
        self.position = position
        self.direction = direction
        self.velocity = velocity
        self.sprite = sprite
        self.radius = radius

    def move(self):
        """
        Перемещает игровой объект
        """
        new_position = self.position + self.direction * self.velocity
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
    ship_stay = load_sprite("ship_stay")
    ship_move = load_sprite("ship_move")
    nothing = load_sprite("nothing")

    def __init__(self, add_bullet):
        """
        Конструктор корабля
        :param add_bullet: callback на добавление пуль
        """
        # last_direction - направление инерции корабля
        self.last_direction = Vector2()
        self.add_bullet = add_bullet
        super().__init__(0, Vector2(0, -1),
                         Vector2(WIDTH / 2, HEIGHT / 2),
                         load_sprite("ship_stay"),
                         10)

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
        self.velocity = SHIP_MAX_VELOCITY
        self.last_direction.update(self.direction)
        self.sprite = self.ship_move

    def shoot(self):
        """
        Корабль стреляет в перед собой
        """
        bullet = Bullet(self.position, BULLET_SPEED, self.direction)
        self.add_bullet(bullet)

    def decrease_velocity(self):
        """
        Замедляет корабль
        """
        if self.velocity - SHIP_MIN_VELOCITY > 0:
            self.velocity -= self.velocity / SHIP_DECELERATION_FACTOR
        else:
            self.velocity = 0

    def draw(self, screen):
        """
        Отрисовка корабля на экране
        :param screen: экран
        """
        angle = self.direction.angle_to(Vector2(0, -1))
        ship = pygame.transform.rotate(self.sprite, angle + 90)
        ship_rect = ship.get_rect(center=self.position)
        screen.blit(ship, ship_rect)

        self.sprite = self.ship_stay

    def move(self):
        """
        Перемещает корабль
        """
        new_position = self.position + self.last_direction * self.velocity
        self.position = wrap_position(new_position)

    def change_sprites(self):
        self.sprite = self.nothing


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
        velocity, direction = get_random_vel_dir(MIN_ASTEROID_VELOCITY,
                                                 MAX_ASTEROID_VELOCITY)
        super().__init__(velocity, direction, position,
                         sprite_for_asteroid(size_name),
                         ASTEROID_RADII.get(size_name))

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

    def __init__(self, position, velocity, direction):
        """
        Конструктор
        :param position: Первоначальная позиция пули
        :param velocity: Скорость пули
        :param direction: Направление движения пули
        """
        new_direction = Vector2(0, 0)
        new_direction.update(direction)
        super().__init__(velocity, new_direction,
                         position, load_sprite('bullet'), 3)

    def move(self):
        """
        Перемещает пулю
        """
        self.position = self.position + self.direction * self.velocity


class UFO(GameObject):
    """
    Класс нло, штука стреляет в игрока
    """

    def __init__(self, position, add_bullets):
        self.add_bullets = add_bullets
        velocity, direction = get_random_vel_dir(UFO_MIN_VELOCITY,
                                                 UFO_MAX_VELOCITY)
        super().__init__(velocity, direction, position, load_sprite('ufo'), UFO_RADIUS)

    def shoot_at(self, ship_position: Vector2):
        """
        Создает пулю в направлении корабля с некоторым разбросом
        :param ship_position: координаты корабля
        :return:
        """
        vector_to_ship = ship_position - self.position
        new_bullet = Bullet(self.position, BULLET_SPEED / 2,
                            randomize_vector_direction(vector_to_ship))
        self.add_bullets(new_bullet)

    def change_velocity(self):
        """
        Изменяет скорость и направление
        """
        self.velocity, self.direction = get_random_vel_dir(UFO_MIN_VELOCITY,
                                                           UFO_MAX_VELOCITY)


# booster
# records
