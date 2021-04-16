import pygame
import KineticButton

from pygame.locals import *


class MainMenu:
    def __init__(self, screen):
        self.hover = 0
        self.options = [KineticButton.KineticButton("Nouvelle Scène", 100, 50, 500, 100, "new", background_color=(255, 255, 255), outline=1),
                        KineticButton.KineticButton("Ouvrir Scène", 100, 300, 500, 100, "open", background_color=(255, 255, 255), outline=1)]
        self.screen = screen

    def render(self):
        """Fonction s'occupant de faire un rendu à l'écran"""

        # Admettons, nous utiliserons un fond noir
        self.screen.fill((0, 0, 0))

        # Désormais, nous devons afficher nos bouttons
        for button in self.options:
            button.render(self.screen)

        pygame.display.update()

    def _update_hover_keyboard(self, key):
        self.options[self.hover].set_is_hover(False)

        if key == K_UP:
            if self.hover == 0:
                self.hover = len(self.options) - 1
            else:
                self.hover -= 1
        elif key == K_DOWN:
            if self.hover == len(self.options) - 1:
                self.hover = 0
            else:
                self.hover += 1

        self.options[self.hover].set_is_hover(True)

    def _update_hover_mouse(self, mouse_pos):
        self.options[self.hover].set_is_hover(False)
        is_on_button = False
        for i in range(len(self.options)):
            if self.options[i].do_hover(mouse_pos):
                is_on_button = True
                self.hover = i
        return is_on_button

    def start(self):
        """
        Fonction s'occupant de la boucle du menu principal
        :return: Action choisie (Ouvrir Scène/Nouvelle scène)
        """
        is_in_menu = True

        self.render()
        while is_in_menu:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return ["quit", ]
                if event.type == KEYDOWN:
                    self._update_hover_keyboard(event.key)
                    self.render()
                    if event.key in [K_RETURN, K_SPACE]:
                        val = self.options[self.hover].get_value()
                        if val == "new":
                            return ["create_scene", ]
                        else:
                            return ["open_scene", ]
                if event.type == MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self._update_hover_mouse(mouse_pos)
                    self.render()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and self._update_hover_mouse(pygame.mouse.get_pos()):  # Clique Gauche
                        val = self.options[self.hover].get_value()
                        if val == "new":
                            return ["create_scene", ]
                        else:
                            return ["choose_scene", ]
