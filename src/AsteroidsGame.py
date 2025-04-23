import pygame

from resources.SpritesManager import SpritesManager
from resources.constants import MAIN_MENU_STATE
from src.Controller import Controller
from src.Game import GameModel
from src.ResultsManager import ResultsManager
from src.View import View


class AsteroidsGame:
    """
    Класс со всей общей логикой
    """

    def __init__(self):
        pygame.init()
        results_manager = ResultsManager()
        SpritesManager.init_default_sprites()
        self.model = GameModel()
        self.view = View(self.model, results_manager)
        self.controller = Controller(self.model, self.change_game_state, self.change_pixel_rate, results_manager)
        self.game_state: int = MAIN_MENU_STATE

    def loop(self):
        """
        main loop
        """
        while True:
            self.controller.process_events(self.game_state)
            self.model.update(self.game_state)
            self.view.draw(self.game_state)

    def change_game_state(self, state_name):
        self.game_state = state_name

    def change_pixel_rate(self, pixel_rate):
        self.view.change_pixel_rate(pixel_rate)
