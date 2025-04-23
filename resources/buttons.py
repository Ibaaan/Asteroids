import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UITextBox, UIHorizontalSlider

from resources.constants import GAME_RUN_EVENT, LEADERBOARD_EVENT, SCREEN_HEIGHT, SCREEN_WIDTH, \
    BACK_FROM_LEADERBOARD_EVENT, SAVE_RESULT_EVENT


class Buttons:
    _dragged = False
    _pixel_rate = 1

    MANAGER: UIManager
    NEW_GAME_BUTTON: UIButton
    LEADERBOARD_BUTTON: UIButton
    SAVE_RESULT_BUTTON: UIButton
    BACK_FROM_LEADERBOARD_BUTTON: UIButton
    LEADERBOARD: UITextBox
    GRAPHICS_SLIDER: UIHorizontalSlider

    @classmethod
    def process_buttons(cls, event):

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == cls.NEW_GAME_BUTTON:
                pygame.event.post(pygame.event.Event(GAME_RUN_EVENT))

            elif event.ui_element == cls.LEADERBOARD_BUTTON:
                pygame.event.post(pygame.event.Event(LEADERBOARD_EVENT))

            elif event.ui_element == cls.SAVE_RESULT_BUTTON:
                pygame.event.post(pygame.event.Event(SAVE_RESULT_EVENT))

            elif event.ui_element == cls.BACK_FROM_LEADERBOARD_BUTTON:
                pygame.event.post(pygame.event.Event(BACK_FROM_LEADERBOARD_EVENT))

        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == cls.GRAPHICS_SLIDER:
                cls._dragged = True

        cls.MANAGER.process_events(event)

    @classmethod
    def init_buttons(cls):
        cls.MANAGER = pygame_gui.UIManager(window_resolution=(800, 600))

        cls.NEW_GAME_BUTTON = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2),
                (200, 80)),
            text='New Game',
            manager=cls.MANAGER)

        cls.LEADERBOARD_BUTTON = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 80 + 10),
                (200, 80)),
            text='Leaderboard',
            manager=cls.MANAGER)

        cls.SAVE_RESULT_BUTTON = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 160 + 20),
                (200, 80)),
            text='Save Result',
            manager=cls.MANAGER)

        cls.BACK_FROM_LEADERBOARD_BUTTON = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (20, SCREEN_HEIGHT - 80),
                (100, 60)),
            text='Back To Menu',
            manager=cls.MANAGER)

        cls.LEADERBOARD = UITextBox(
            html_text="",
            relative_rect=pygame.Rect(140, 44 + 57, SCREEN_WIDTH - 280, SCREEN_HEIGHT - (44 + 57)),
            manager=cls.MANAGER)



        cls.show_main_menu()

    @classmethod
    def disable_all(cls):
        cls.NEW_GAME_BUTTON.disable()
        cls.NEW_GAME_BUTTON.visible = 0

        cls.LEADERBOARD_BUTTON.disable()
        cls.LEADERBOARD_BUTTON.visible = 0

        cls.SAVE_RESULT_BUTTON.disable()
        cls.SAVE_RESULT_BUTTON.visible = 0

        cls.BACK_FROM_LEADERBOARD_BUTTON.disable()
        cls.BACK_FROM_LEADERBOARD_BUTTON.visible = 0

        cls.LEADERBOARD.disable()
        cls.LEADERBOARD.visible = 0

        cls._disable_graphic_slider()

    @classmethod
    def _enable_graphic_slider(cls):
        cls.GRAPHICS_SLIDER = UIHorizontalSlider(
            relative_rect=pygame.Rect(
                (SCREEN_WIDTH / 2 - 300, SCREEN_HEIGHT / 2 + 160 + 20 + 46),
                (600, 20)),
            start_value=cls._pixel_rate,
            value_range=(1, 6),
            manager=cls.MANAGER
        )

    @classmethod
    def show_main_menu(cls):
        cls.disable_all()

        cls.NEW_GAME_BUTTON.enable()
        cls.NEW_GAME_BUTTON.visible = 1

        cls.LEADERBOARD_BUTTON.enable()
        cls.LEADERBOARD_BUTTON.visible = 1

        cls._enable_graphic_slider()

    @classmethod
    def show_game_over(cls):
        cls.disable_all()

        cls.NEW_GAME_BUTTON.enable()
        cls.NEW_GAME_BUTTON.visible = 1

        cls.LEADERBOARD_BUTTON.enable()
        cls.LEADERBOARD_BUTTON.visible = 1

        cls.SAVE_RESULT_BUTTON.enable()
        cls.SAVE_RESULT_BUTTON.visible = 1

    @classmethod
    def show_leaderboard(cls, scores):
        cls.disable_all()

        cls.BACK_FROM_LEADERBOARD_BUTTON.enable()
        cls.BACK_FROM_LEADERBOARD_BUTTON.visible = 1

        cls.LEADERBOARD.appended_text = "\n".join([f"{name} - {score}" for name, score in scores])
        cls.LEADERBOARD.rebuild()

        cls.LEADERBOARD.enable()
        cls.LEADERBOARD.visible = 1

    @classmethod
    def show_save_result(cls):
        cls.disable_all()

        cls.BACK_FROM_LEADERBOARD_BUTTON.enable()
        cls.BACK_FROM_LEADERBOARD_BUTTON.visible = 1

    @classmethod
    def pixel_rate(cls) -> int:
        if cls._dragged:
            cls._dragged = False
            return cls.GRAPHICS_SLIDER.get_current_value()
        return -1

    @classmethod
    def _disable_graphic_slider(cls):
        try:
            cls._pixel_rate = cls.GRAPHICS_SLIDER.get_current_value()
            cls.GRAPHICS_SLIDER.kill()
        except AttributeError:
            # ignore
            pass


