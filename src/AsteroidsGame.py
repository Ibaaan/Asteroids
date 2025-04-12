import pygame

from resources.settings import (HEIGHT, WIDTH, ENTER_NAME, SHOW_TABLE)
from src.Model import Model, Controller
from src.Results import Results

# TODO Отделить меню от логики
class AsteroidsGame:
    """
    Класс со всей общей логикой
    """

    def __init__(self):
        self.view = View()
        self.model = Model()
        self.controller = Controller(self.model)
        self.clock = pygame.time.Clock()

    def loop(self):
        """
        main loop
        """
        while True:
            self.controller.process_events()
            self.model.update()
            self.view.draw(self.model)
            self.clock.tick(60)


class View:
    """
    Класс изображающий объекты на экране
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Asteroids")

    def draw(self, model):
        """
        Отображает всё
        """
        self.screen.fill('black')
        if model.run:
            for obj in model.get_game_objects():
                obj.draw(self.screen)

            self.print_statistics(model.score, model.lives)
        elif model.saving_results:
            if model.saving_results == ENTER_NAME:
                model.results.draw_enter_name(self.screen)
            elif model.saving_results == SHOW_TABLE:
                model.results.draw_table(self.screen)
        else:
            self.game_over_screen(model.score)
        pygame.display.flip()

    def game_over_screen(self, score):
        """
        Рисует экран окончания игры
        """
        font = pygame.font.SysFont('couriernew', 60)
        lost = font.render('YOU LOST', True, 'white')
        lost_rect = lost.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.screen.blit(lost, lost_rect)

        score = font.render(str(score), True, 'white')
        score_rect = score.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 60))
        self.screen.blit(score, score_rect)

        font = pygame.font.SysFont('couriernew', 40)
        space = font.render('R to restart', True, 'white')
        space_rect = space.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 180))
        self.screen.blit(space, space_rect)

        results = font.render('P to results', True, 'white')
        results_rect = space.get_rect(center=(WIDTH / 2, score.get_height()))
        self.screen.blit(results, results_rect)

    def print_statistics(self, score, lives):
        """
        Рисует счет игрок в левом верхнем углу
        """
        font = pygame.font.SysFont('couriernew', 40)
        score = font.render(str(score), True, 'white')
        self.screen.blit(score, (0, 0))

        lives = font.render("Lives:" + str(lives), True, 'white')
        self.screen.blit(lives, (0, score.get_height()))

