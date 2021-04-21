import pygame
from pygame.locals import *
from InputText import InputText
from CheckBox import CheckBox


class NewSceneAsk:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        font = pygame.font.SysFont("Calibri", 25)
        self.text_name = font.render("Entrez le nom de la prochaine scène :", False, (255, 255, 255))
        self.input_name = InputText(140, 345, 1000, 30, text_color=(255, 255, 255), background_color=(173, 173, 173, 128), outline_color=(0, 0, 0), outline=1, font_size=25)

        self.text_type = font.render("La scène est un choix :", False, (255, 255, 255))
        self.check_type = CheckBox(500, 500)

    def render(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.text_name, (140, 200))
        self.screen.blit(self.text_type, (140, 500))

        self.input_name.render(self.screen)
        self.check_type.render(self.screen)

        pygame.display.update()

    def start(self):
        in_menu = True

        self.render()
        while in_menu:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return ['quit', ]

                if event.type == MOUSEBUTTONDOWN:
                    if self.check_type.do_hover(pygame.mouse.get_pos()):
                        self.check_type.click()
                        self.render()

                if event.type == TEXTINPUT:
                    self.input_name.type(event)
                    self.render()

                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return [self.input_name.get_value(), self.check_type.get_value()]
                    else:
                        self.input_name.special_type(event)
                        self.render()
