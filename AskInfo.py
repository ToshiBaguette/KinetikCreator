import InputText
import pygame
from pygame.locals import *


class AskInfo:
    def __init__(self, screen, question="Entrez le nom de la scène: "):
        self.screen = screen
        self.input = InputText.InputText(140, 345, 1000, 30, text_color=(255, 255, 255), background_color=(173, 173, 173, 128), outline_color=(0, 0, 0), outline=1, font_size=25)
        self.error = None
        self.text = pygame.font.SysFont("Calibri", 25).render(question, False, (255, 255, 255))

    def render(self):
        self.screen.fill((0, 0, 0))
        if self.error:
            self.screen.blit(self.error, (140, 250))
        self.screen.blit(self.text, (140, 200))
        self.input.render(self.screen)
        pygame.display.update()

    def start(self, error=""):
        if len(error) > 0:
            self.error = pygame.font.SysFont("Calibri", 25).render(error, False, (220, 70, 70))
        is_typing = True

        self.render()
        while is_typing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return ["quit", ]
                if event.type == TEXTINPUT:
                    self.input.type(event)
                    self.render()
                if event.type == KEYDOWN and event.key == K_RETURN:
                    return self.input.get_value()
                elif event.type == KEYDOWN:
                    self.input.special_type(event)
                    self.render()
