import json

import pygame

from resources.settings import WIDTH, HEIGHT, ENTER_NAME, SHOW_TABLE


class Results:
    """
    Отвечает за сохранения и отображения таблицы результатов
    """

    filename = "resources/scores.json"

    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.input_box = pygame.Rect((WIDTH - 200) // 2, (HEIGHT - 40) // 2, 200, 40)
        self.input_text = ''
        self.input_active = True

    def handle_event(self, event, score):
        if event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_RETURN:
                    self.save_text(score)
                    self.input_text = ''
                    return SHOW_TABLE
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
        return ENTER_NAME

    def save_text(self, score):
        data = self.get_score()

        data[self.input_text] = score

        with open(self.filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def draw_enter_name(self, screen):
        txt_surface = self.font.render(self.input_text, True, pygame.Color('dodgerblue2'))
        width_txt = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width_txt
        pygame.draw.rect(screen, pygame.Color('dodgerblue2'), self.input_box, 2)
        screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))

    def draw_table(self, screen):
        scores = self.get_score()

        font = pygame.font.Font(None, 36)
        y_offset = 50

        for name, score in scores.items():
            score_text = f"{name}: {score}"
            text_surface = font.render(score_text, True, (255, 255, 255))
            screen.blit(text_surface, ((WIDTH - 200) // 2, y_offset))
            y_offset += 40

    def get_score(self, ):
        with open(self.filename, 'r') as json_file:
            data = json.load(json_file)
        return data
