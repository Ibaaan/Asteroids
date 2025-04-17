import pygame
from pygame import Surface, SurfaceType
from pygame_widgets.button import ButtonArray

from resources.settings import GAME_RUN_STATE, SCREEN_WIDTH, MAIN_MENU_STATE, GAME_RUN_EVENT, \
    LEADERBOARD_EVENT, GAME_OVER_STATE, SCREEN_HEIGHT
from src.Game import GameModel


class MenuButtons:
    main_menu_buttons: ButtonArray
    game_over_buttons: ButtonArray

    def __init__(self, screen: Surface | SurfaceType):
        self.init_buttons(screen)

    def init_buttons(self, screen: Surface | SurfaceType):
        self.game_over_buttons = ButtonArray(
            win=screen,
            x=50,
            y=200,  # gud
            width=500,
            height=300,
            shape=(1, 4),
            border=10,
            texts=('New game',
                   'Leaderboard',
                   'Save result',
                   'Exit'),
            onClicks=(self._new_game,
                      self._show_leaderboard,
                      self._save_result,
                      self._game_exit)
        )

        self.main_menu_buttons = ButtonArray(
            win=screen,
            x=50,
            y=50,
            width=500,
            height=500,
            shape=(1, 3),
            border=10,
            texts=('New game',
                   'Leaderboard',
                   'Exit'),
            onClicks=(self._new_game,
                      self._show_leaderboard,
                      self._game_exit)
        )

    def _game_exit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _new_game(self):
        pygame.event.post(GAME_RUN_EVENT)

    def _show_leaderboard(self):
        pygame.event.post(LEADERBOARD_EVENT)

    def _save_result(self):
        # TODO
        print("results saved")

    def draw_main_menu(self):
        self.main_menu_buttons.draw()

    def draw_game_over(self):
        self.game_over_buttons.draw()


class View:
    """
    Класс изображающий объекты на экране
    """

    def __init__(self, model: GameModel):

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Asteroids")
        self.model = model
        self.menu_buttons = MenuButtons(screen=self.screen)

    def draw(self, game_state: int):
        """
        Отображает всё
        """
        self.screen.fill('black')

        if game_state == GAME_RUN_STATE:
            for obj in self.model.get_game_objects():
                obj.draw(self.screen)
            self.print_statistics(self.model.score, self.model.lives)
        elif game_state == MAIN_MENU_STATE:
            self.menu_buttons.draw_main_menu()
        elif game_state == GAME_OVER_STATE:
            self.menu_buttons.draw_game_over()
            self.game_over_screen(self.model.score)
        #
        #     self.print_statistics(model.score, model.lives)
        # elif model.saving_results:
        #     if model.saving_results == ENTER_NAME:
        #         model.results.draw_enter_name(self.screen)
        #     elif model.saving_results == SHOW_TABLE:
        #         model.results.draw_table(self.screen)
        # else:
        #     self.game_over_screen(model.score)
        pygame.display.flip()

    def game_over_screen(self, score):
        """
        Рисует экран окончания игры
        """
        font = pygame.font.SysFont('couriernew', 60)
        lost = font.render('YOU LOST', True, 'white')
        lost_rect = lost.get_rect(center=(SCREEN_WIDTH / 2, lost.get_height()))
        self.screen.blit(lost, lost_rect)

        score = font.render('Your Score: ' + str(score), True, 'white')
        score_rect = score.get_rect(center=(SCREEN_WIDTH / 2,
                                            score.get_height() + lost.get_height()))
        self.screen.blit(score, score_rect)

    def print_statistics(self, score, lives):
        """
        Рисует счет игрок в левом верхнем углу
        """
        font = pygame.font.SysFont('couriernew', 40)
        score = font.render(str(score), True, 'white')
        self.screen.blit(score, (0, 0))

        lives = font.render("Lives:" + str(lives), True, 'white')
        self.screen.blit(lives, (0, score.get_height()))
