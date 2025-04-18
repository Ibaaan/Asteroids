import pygame

from resources.buttons import Buttons
from resources.settings import GAME_RUN_STATE, SCREEN_WIDTH, MAIN_MENU_STATE, GAME_OVER_STATE, SCREEN_HEIGHT, \
    SAVE_RESULT_STATE, LEADERBOARD_STATE
from src.Game import GameModel
from src.ResultsManager import ResultsManager


# class MenuButtons:
#     main_menu_buttons: ButtonArray
#     game_over_buttons: ButtonArray
#
#     def __init__(self, screen: Surface | SurfaceType):
#         self.init_buttons(screen)
#
#     def init_buttons(self, screen: Surface | SurfaceType):
#         self.game_over_buttons = ButtonArray(
#             win=screen,
#             x=50,
#             y=200,  # gud
#             width=500,
#             height=300,
#             shape=(1, 4),
#             border=10,
#             texts=('New game',
#                    'Leaderboard',
#                    'Save Results',
#                    'Exit'),
#             onClicks=(lambda: print(1),
#                       lambda: print(2),
#                       lambda: print(3),
#                       lambda: print(4))
#         )
#
#         self.new_game_button = Button(
#
#         )
#
#
#         self.main_menu_buttons = ButtonArray(
#             win=screen,
#             x=50,
#             y=50,
#             width=500,
#             height=500,
#             shape=(1, 3),
#             border=10,
#             texts=('New game',
#                    'Leaderboard',
#                    'Exit'),
#             onClicks=(self._new_game,
#                       self._show_leaderboard,
#                       self._game_exit)
#         )
#
#     def _game_exit(self):
#         print("Exit")
#         pygame.event.post(pygame.event.Event(pygame.QUIT))
#
#     def _new_game(self):
#         pygame.event.post(GAME_RUN_EVENT)
#
#     def _show_leaderboard(self):
#         # pygame.event.post(LEADERBOARD_EVENT)
#         print('results')
#
#     def _save_result(self):
#         pygame.event.post(LEADERBOARD_EVENT)
#         print("results saved")
#
#     def draw_main_menu(self):
#         self.main_menu_buttons.draw()
#
#     def draw_game_over(self):
#         self.game_over_buttons.draw()


class View:
    """
    Класс изображающий объекты на экране
    """

    def __init__(self, model: GameModel, results_manager:ResultsManager):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Asteroids")
        self.model = model
        self.results_manager = results_manager
        Buttons.init_buttons()



    def draw(self, game_state: int):
        """
        Отображает всё
        """
        time_delta = self.clock.tick(60) / 1000.0
        Buttons.MANAGER.update(time_delta)

        self.screen.fill('black')



        if game_state == GAME_RUN_STATE:
            for group in self.model.get_game_objects_grouped():
                group.update()
                # for sprite in group:
                #     print(sprite)
                #     try:
                #         print(f"Sprite Name: {sprite.name}, Position: {sprite.rect.topleft}")
                #     except AttributeError as e:
                #         print(e)
                group.draw(self.screen)
            # raise AttributeError
            self.print_statistics(self.model.score, self.model.lives)

        elif game_state == MAIN_MENU_STATE:
            self._show_game_name()

        elif game_state == GAME_OVER_STATE:
            self.game_over_screen(self.model.score)

        elif game_state == SAVE_RESULT_STATE:
            self.results_manager.draw_enter_name(self.screen)

        elif game_state == LEADERBOARD_STATE:
            self._show_leaderboard_name()

        Buttons.MANAGER.draw_ui(self.screen)
        pygame.display.flip()

    def _show_game_name(self):
        game_name = (pygame.font.SysFont('couriernew', 80)
                     .render('ASTEROIDS', True, 'white'))
        game_name_rect = game_name.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
        self.screen.blit(game_name, game_name_rect)

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

    def _show_leaderboard_name(self):
        leaderboard_name = (pygame.font.SysFont('couriernew', 50)
                     .render('Leaderboard', True, 'white'))
        leaderboard_rect = leaderboard_name.get_rect(center=(SCREEN_WIDTH / 2, 50))
        self.screen.blit(leaderboard_name, leaderboard_rect)
