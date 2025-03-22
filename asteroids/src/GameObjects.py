import pygame
from pygame.math import Vector2

from asteroids.resources.settings import (WIDTH,
                                          HEIGHT,
                                          ANGULAR_VELOCITY,
                                          MAX_VELOCITY,
                                          BULLET_SPEED,
                                          DECELERATION_FACTOR,
                                          DBL_EPSILON, ASTEROID_RADIUSES,
                                          MIN_ASTEROID_V, MAX_ASTEROID_V)
from asteroids.resources.utils import (wrap_position,
                                       get_random_vel_dir,
                                       load_sprite,
                                       sprite_for_asteroid)


class _GameObject:
    def __init__(self, velocity: float, direction: Vector2,
                 position: Vector2, sprite, radius):
        self.position = position
        self.direction = direction
        self.velocity = velocity
        self.sprite = sprite
        self.radius = radius

    def move(self):
        new_position = self.position + self.direction * self.velocity
        self.position = wrap_position(new_position)

    def draw(self, screen):
        blit_position = self.position - Vector2(self.radius)
        screen.blit(self.sprite, blit_position)

    def collides_with(self, object):
        distance = self.position.distance_to(object.position)
        return distance < self.radius + object.radius


class Ship(_GameObject):
    def __init__(self, create_bullet):

        self.last_direction = Vector2()
        self.create_bullet = create_bullet
        super().__init__(0, Vector2(0, -1),
                         Vector2(WIDTH / 2, HEIGHT / 2),
                         load_sprite("ship_stay"),
                         10)

    def rotate(self, clockwise):
        """
        :param clockwise: if true -> rotate clockwise,
        else rotate counterclockwise
        """
        sign = 1 if clockwise else -1
        self.direction.rotate_ip(ANGULAR_VELOCITY * sign)

    def accelerate(self):
        self.velocity = MAX_VELOCITY
        self.last_direction.update(self.direction)
        self.sprite = load_sprite("ship_move")

    def shoot(self):
        bullet = Bullet(self.position, BULLET_SPEED, self.direction)
        self.create_bullet(bullet)

    def decrease_velocity(self):
        if self.velocity - DBL_EPSILON > 0:
            self.velocity -= self.velocity / DECELERATION_FACTOR
        else:
            self.velocity = 0

    def draw(self, screen):
        angle = self.direction.angle_to(Vector2(0, -1))
        ship = pygame.transform.rotate(self.sprite, angle + 90)
        ship_rect = ship.get_rect(center=self.position)
        screen.blit(ship, ship_rect)
        self.sprite = load_sprite("ship_stay")

    def move(self):
        new_position = self.position + self.last_direction * self.velocity
        self.position = wrap_position(new_position)


class Asteroid(_GameObject):
    def __init__(self, size_name, position, create_asteroid):
        """
        :param size_name: BIG, MEDIUM, SMALL
        """
        self.create_asteroid = create_asteroid
        self.size_name = size_name
        velocity, direction = get_random_vel_dir(MIN_ASTEROID_V,
                                                 MAX_ASTEROID_V)
        super().__init__(velocity, direction, position,
                         sprite_for_asteroid(size_name),
                         ASTEROID_RADIUSES.get(size_name))

    def split(self):
        if self.size_name > 1:
            for _ in range(2):
                self.create_asteroid(
                    Asteroid(self.size_name - 1,
                             self.position, self.create_asteroid))


class Bullet(_GameObject):
    def __init__(self, position, velocity, direction):
        new_direction = Vector2(0, 0)
        new_direction.update(direction)
        super().__init__(velocity, new_direction,
                         position, load_sprite('bullet'), 3)

    def move(self):
        self.position = self.position + self.direction * self.velocity
