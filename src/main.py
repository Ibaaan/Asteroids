import os

from AsteroidsGame import AsteroidsGame


def main():
    asteroids = AsteroidsGame()
    asteroids.loop()


if __name__ == "__main__":
    print()
    print(os.getcwd())
    print()
    main()
