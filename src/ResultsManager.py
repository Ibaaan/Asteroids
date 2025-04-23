import json

import pygame

from resources.constants import SCREEN_WIDTH, SCREEN_HEIGHT, LEADERBOARD_EVENT


class ResultsManager:
    """
    Отвечает за сохранения и отображения таблицы результатов
    """

    filename = "resources/scores.json"

    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.input_box = pygame.Rect((SCREEN_WIDTH - 200) // 2, (SCREEN_HEIGHT - 40) // 2, 200, 40)
        self.input_text = ''
        self.input_active = True

    def write_name_controller(self, event, score):
        if event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_RETURN:
                    self.save_text(score)
                    pygame.event.post(pygame.event.Event(LEADERBOARD_EVENT))
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

    def save_text(self, score):
        data = self._get_data()

        data[self.input_text] = score
        self.input_text = ''

        with open(self.filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def draw_enter_name(self, screen):
        txt_surface = self.font.render(self.input_text, True, pygame.Color('dodgerblue2'))
        width_txt = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width_txt
        pygame.draw.rect(screen, pygame.Color('dodgerblue2'), self.input_box, 2)
        screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))

    def _get_data(self):
        with open(self.filename, 'r') as json_file:
            data = json.load(json_file)
        return data

    def get_all_scores(self):
        data = self._get_data()
        scores = []
        for key in data:
            scores.append((key, int(data[key])))
        return sorted(scores, key=lambda x: x[1], reverse=True)
