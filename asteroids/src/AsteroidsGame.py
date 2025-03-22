import pygame

from asteroids.src.resources.settings import (HEIGHT, WIDTH,
                                              CLOCKWISE, COUNTER_CLOCKWISE,
                                              ASTEROIDS_SCORE,
                                              MIN_ASTEROID_DISTANCE, BIG)
from asteroids.src.resources.utils import get_random_position
from asteroids.src.GameObjects import Ship, Asteroid


class AsteroidsGame:

    def __init__(self):
        self.level = None
        self.run = None
        self.score = None
        self.ship = None
        self.bullets = None
        self.asteroids = None
        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Asteroids")

        self.init_game_objects()

    def loop(self):
        """
        main loop
        """
        while True:
            self._controller()
            if self.run:
                self._model()
            self._view()
            self.clock.tick(60)

    def _controller(self):
        """
        processes inputs
        """
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.ship.shoot()
                if e.key == pygame.K_r:
                    self.init_game_objects()

        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_d]:
            self.ship.rotate(CLOCKWISE)
        if is_key_pressed[pygame.K_a]:
            self.ship.rotate(COUNTER_CLOCKWISE)
        if is_key_pressed[pygame.K_w]:
            self.ship.accelerate()

    def _model(self):
        self._calc_collisions()
        self._move_objects()
        self.ship.decrease_velocity()

        if not self.asteroids:
            self.level += 1
            self.create_asteroids()

    def _view(self):
        self.screen.fill('black')
        if self.run:
            for obj in self._get_game_objects():
                obj.draw(self.screen)

            self.print_score()
        else:
            self.game_over_screen()
        pygame.display.flip()

    def _calc_collisions(self):

        for asteroid in self.asteroids:
            if asteroid.collides_with(self.ship):
                self.run = False

        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if asteroid.collides_with(bullet):
                    self.score += ASTEROIDS_SCORE[asteroid.size_name]
                    self.asteroids.remove(asteroid)
                    try:
                        self.bullets.remove(bullet)
                    except ValueError as e:
                        print(e)

                    asteroid.split()

        if len(self.bullets) > 4:
            self.bullets.pop(0)

    def _move_objects(self):
        for _ in self._get_game_objects():
            _.move()

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets, self.ship]
        return game_objects

    def init_game_objects(self):
        self.asteroids = []
        self.bullets = []
        self.ship = Ship(self.bullets.append)
        self.score = 0
        self.run = True
        self.level = 1
        self.create_asteroids()

    def create_asteroids(self):
        for _ in range(2 + self.level):
            while True:
                position = get_random_position()
                if (
                        position.distance_to(self.ship.position)
                        > MIN_ASTEROID_DISTANCE
                ):
                    break
            self.asteroids.append(Asteroid(BIG, position,
                                           self.asteroids.append))

    def game_over_screen(self):
        font = pygame.font.SysFont('couriernew', 60)
        lost = font.render('YOU LOST', True, 'white')
        lost_rect = lost.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.screen.blit(lost, lost_rect)

        score = font.render(str(self.score), True, 'white')
        score_rect = score.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 60))
        self.screen.blit(score, score_rect)

        font = pygame.font.SysFont('couriernew', 40)
        space = font.render('R to restart', True, 'white')
        space_rect = score.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 180))
        self.screen.blit(space, space_rect)

    def print_score(self):
        font = pygame.font.SysFont('couriernew', 40)
        score = font.render(str(self.score), True, 'white')
        self.screen.blit(score, (0, 0))
