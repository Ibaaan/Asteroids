from AsteroidsGame import AsteroidsGame


def main():
    try:
        asteroids = AsteroidsGame()
        asteroids.loop()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
