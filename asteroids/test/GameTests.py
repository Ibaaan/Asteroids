import unittest

from pygame import Vector2

from asteroids.src.AsteroidsGame import AsteroidsGame
from asteroids.src.GameObjects import Bullet, Asteroid


class AsteroidsGameTest(unittest.TestCase):
    def setUp(self):
        self.asteroid_game = AsteroidsGame()

    def test_create_asteroids(self):
        self.asteroid_game.asteroids = []
        self.asteroid_game.level = 1
        self.asteroid_game.create_asteroids()
        self.assertEqual(len(self.asteroid_game.asteroids), 1 + 2)
        self.assertTrue(self.asteroid_game.asteroids[1]
                        .position.distance_to(self.asteroid_game.ship.position)
                        > 200)

    def test_init_game_objects(self):
        self.asteroid_game.init_game_objects()

        self.assertEqual(self.asteroid_game.bullets, [])
        self.assertTrue(self.asteroid_game.ship is not None)
        self.assertEqual(self.asteroid_game.score, 0)
        self.assertEqual(self.asteroid_game.run, True)
        self.assertEqual(self.asteroid_game.level, 1)

    def test_get_game_objects(self):
        asteroids = self.asteroid_game.asteroids
        self.asteroid_game.bullets.append(Bullet(Vector2(0.0), 0,
                                                 Vector2(0.0)))
        bullets = self.asteroid_game.bullets
        game_objects = self.asteroid_game._get_game_objects()
        self.assertEqual(game_objects, [*asteroids, *bullets,
                                        self.asteroid_game.ship])

    def test_calc_collisions(self):
        asteroid = Asteroid(3,
                            self.asteroid_game.ship.position,
                            self.asteroid_game.asteroids.append)
        self.asteroid_game.asteroids.append(asteroid)
        self.asteroid_game._calc_collisions()

        self.assertEqual(self.asteroid_game.run, False)

        bullet = Bullet(
            self.asteroid_game.ship.position, 0, Vector2())
        self.asteroid_game.bullets.append(bullet)
        self.asteroid_game._calc_collisions()

        self.assertTrue(asteroid not in self.asteroid_game.asteroids)
        self.assertTrue(bullet not in self.asteroid_game.bullets)
