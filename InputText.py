import utils
import pygame
from pygame.locals import *


class InputText:
    def __init__(self, x, y, width, height, default_text="", background_color=(200, 200, 200), selected_color=(255, 255, 255), text_color=(0, 0, 0), outline=0, outline_color=(0, 0, 0), font="Calibri", font_size=20, selected=True):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = default_text
        self.background_color = background_color
        self.text_color = text_color
        self.outline = outline
        self.outline_color = outline_color
        self.font = pygame.font.SysFont(font, font_size)
        self.selected = selected
        self.selected_color = selected_color
        self.cursor = len(self.text)

    def special_type(self, event):
        if event.key == K_RETURN:
            self.text += "\n"
        elif event.key == K_BACKSPACE:
            self.delete()
        elif event.key == K_LEFT and self.cursor > 0:
            self.cursor -= 1
        elif event.key == K_RIGHT and self.cursor < len(self.text):
            self.cursor += 1

    def type(self, event):
        self.text = self.text[:self.cursor] + event.text + self.text[self.cursor:]
        self.cursor += 1

    def delete(self):
        self.text = self.text[:self.cursor - 1] + self.text[self.cursor:]
        self.cursor -= 1

    def get_value(self):
        return self.text

    def do_click(self, mouse_pos):
        self.selected = self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height
        return self.selected

    def render(self, screen):
        # On commence par le background
        bgColor = self.background_color
        if self.selected:
            bgColor = self.selected_color

        bgSurface = pygame.Surface((self.width, self.height))
        alpha = 255
        if len(bgColor) > 3:
            alpha = bgColor[3]
        bgSurface.set_alpha(alpha)
        bgSurface.fill(bgColor)

        screen.blit(bgSurface, (self.x, self.y))

        # On doit construire les strings et les font
        lines = utils.wrap_multi_line(self.text, self.font, self.width)
        display_lines = [self.font.render(txt, False,  self.text_color) for txt in lines]
        display_outlines = [self.font.render(txt, False, self.outline_color) for txt in lines]
        pos_cursor = utils.get_cursor_pos(self.cursor, lines)

        # Et finalement on les affiche
        border_y = self.y + self.font.get_height() / 4
        for i in range(len(display_lines)):
            # D'abord les outlines s'il y en a
            if self.outline > 0:
                screen.blit(display_outlines[i], (self.x + 5 - self.outline, border_y))
                screen.blit(display_outlines[i], (self.x + 5 + self.outline, border_y))
                screen.blit(display_outlines[i], (self.x + 5, border_y - self.outline))
                screen.blit(display_outlines[i], (self.x + 5, border_y + self.outline))

            screen.blit(display_lines[i], (self.x + 5, border_y))

            if pos_cursor[1] == i and self.selected:
                cursor_x = self.font.size(lines[i][:pos_cursor[0]])[0] + self.x + 5
                cursor_y = self.font.get_height() * i + border_y
                screen.fill((0, 0, 0), (cursor_x, cursor_y, 1, self.font.get_height()))

            border_y += self.font.get_height() + 10


