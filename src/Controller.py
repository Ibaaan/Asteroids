import sys

import pygame
import pygame_widgets

from resources.settings import CLOCKWISE, COUNTER_CLOCKWISE, ACCELERATE, UFO_UPDATE_EVENT, SHIP_RECOVERY_EVENT, \
    BOOSTER_ENDED, MAIN_MENU_STATE, GAME_RUN_STATE, GAME_OVER_EVENT, GAME_OVER_STATE, GAME_RUN_EVENT, LEADERBOARD_EVENT, \
    LEADERBOARD_STATE
from src.Game import GameModel
from src.View import MenuButtons


class Controller:
    def __init__(self, game_model: GameModel, change_game_state_callback,
                 menu_buttons:MenuButtons):
        self.change_game_state_callback = change_game_state_callback
        self.model = game_model
        self.buttons = menu_buttons

    def process_events(self, game_state):
        """
        Обрабатывает входные события из очереди событий Pygame
        :param game_state: Статус игры, какой контроллер нужно использовать
        """
        events = pygame.event.get()
        print(len(events))
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self._change_game_state(event)
            if game_state == MAIN_MENU_STATE:
                self.buttons.main_menu_buttons.listen(events)
            elif game_state == GAME_RUN_STATE:
                self._game_model_controller(event)
            elif game_state == GAME_OVER_STATE:
                self.buttons.game_over_buttons.listen(events)
            # self._menu_controller(event)
        if game_state == GAME_RUN_STATE:
            self.ship_movement()
        pygame_widgets.update(events)

    def _game_model_controller(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.model.ship_shoot()
        elif event.type == UFO_UPDATE_EVENT:
            self.model.on_ufo_update()
        elif event.type == SHIP_RECOVERY_EVENT:
            self.model.after_death_animation()
        elif event.type == BOOSTER_ENDED:
            self.model.booster_ended()

    # def _menu_controller(self, event):
    #     if event.type == pygame.KEYDOWN:
    #         # TODO Весь закоменченный код вынести в класс обработки Menu
    #         if self.saving_results == ENTER_NAME:
    #             self.saving_results = self.results.handle_event(event, self.score)
    #         elif self.saving_results == SHOW_TABLE and event.key == pygame.K_SPACE:
    #             self.saving_results = EXIT_TABLE
    #     if event.key == pygame.K_SPACE:
    #         self.model.ship_shoot()
    #         if event.key == pygame.K_r:
    #             self._reset_variables()
    #             self._init_game_objects()
    #         if event.key == pygame.K_p and not self.run:
    #             self.saving_results = ENTER_NAME

    def ship_movement(self):
        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_d]:
            self.model.on_ship_input(CLOCKWISE)
        if is_key_pressed[pygame.K_a]:
            self.model.on_ship_input(COUNTER_CLOCKWISE)
        if is_key_pressed[pygame.K_w]:
            self.model.on_ship_input(ACCELERATE)

    def _change_game_state(self, event):
        if event == GAME_RUN_EVENT:
            self.change_game_state_callback(GAME_RUN_STATE)
            self.model.reset_variables()
        elif event == GAME_OVER_EVENT:
            self.change_game_state_callback(GAME_OVER_STATE)
        elif event == LEADERBOARD_EVENT:
            self.change_game_state_callback(LEADERBOARD_STATE)
