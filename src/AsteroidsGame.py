import pygame

from resources.settings import MAIN_MENU_STATE
from src.Controller import Controller
from src.Game import GameModel
from src.View import View


class AsteroidsGame:
    """
    Класс со всей общей логикой
    """

    def __init__(self):
        pygame.init()

        self.model = GameModel()
        self.view = View(self.model)
        self.controller = Controller(self.model, self._change_game_state,
                                     self.view.menu_buttons)
        self.clock = pygame.time.Clock()
        self.game_state:int = MAIN_MENU_STATE

    def loop(self):
        """
        main loop
        """
        while True:
            self.controller.process_events(self.game_state)
            self.model.update(self.game_state)
            self.view.draw(self.game_state)

            self.clock.tick(60)

    def _change_game_state(self, state_name):
        self.game_state = state_name


