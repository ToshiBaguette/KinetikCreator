import os
import pygame
from InputText import InputText
from pygame.locals import *
from AskInfo import AskInfo


class EditChoice:
    def __init__(self, screen: pygame.Surface, json: dict):
        self.menu_display = False
        self.screen = screen

        self.characters = json["personnages"]

        for char in self.characters:
            char["image_dev"] = pygame.image.load(char["image"])

        self.background_text = pygame.font.SysFont("Calibri", 25).render("Background :", False, (255, 255, 255))
        self.background_input = InputText(10, 40, 1000, 30, json["background"],
                                          background_color=(173, 173, 173, 128), outline=1,
                                          outline_color=(0, 0, 0), text_color=(255, 255, 255), selected=False)

        self.background = None
        if len(self.background_input.get_value()) > 0:
            self.background = pygame.transform.scale(
                pygame.image.load("assets/backgrounds/" + self.background_input.get_value()), (1280, 720))

        self.choices = []
        self.next_choices = []
        i = 0
        for choice in json["choices"]:
            # Texte du choix
            self.choices.append(InputText(100, 100 * i + 5 * i + 100, 500, 40, default_text=choice["value"],
                                          background_color=(173, 173, 173, 128), outline=1,
                                          outline_color=(0, 0, 0), text_color=(255, 255, 255), selected=False))
            # Valeur du choix, affichée en appuyant sur shift
            self.next_choices.append(InputText(100, 100 * i + 5 * i + 100, 500, 40, default_text=choice["next"],
                                               background_color=(173, 173, 173, 128), outline=1,
                                               outline_color=(0, 0, 0), text_color=(255, 255, 255), selected=False))
            i += 1

        self.music_text = pygame.font.SysFont("Calibri", 25).render("Musique :", False, (255, 255, 255))
        self.music_input = InputText(10, 220, 1000, 30, json["music"], background_color=(173, 173, 173, 128),
                                     outline=1, outline_color=(0, 0, 0), text_color=(255, 255, 255),
                                     selected=False)

        self.selected_input = None
        self.dragged_char = -1
        self.offset_drag = [0, 0]
        self.displaying_next = False

    def render(self):
        if self.menu_display:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background_text, (10, 10))
            self.background_input.render(self.screen)

            self.screen.blit(self.music_text, (10, 190))
            self.music_input.render(self.screen)
        else:
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((0, 0, 0))

            # On affiche tous les personnages
            for char in self.characters:
                self.screen.blit(char["image_dev"], (char["position"]["x"], char["position"]["y"]))

            # Finalement, on affiche les choix
            if self.displaying_next:
                for choice in self.next_choices:
                    choice.render(self.screen)
            else:
                for choice in self.choices:
                    choice.render(self.screen)

        pygame.display.update()

    def update_selected_input(self, mouse_pos):
        if self.selected_input:
            self.selected_input.selected = False
        self.selected_input = None

        if self.menu_display:
            if self.background_input.do_click(mouse_pos):
                if self.selected_input:
                    self.selected_input.selected = False
                self.selected_input = self.background_input

        else:
            if self.displaying_next:
                for choice in self.next_choices:
                    if choice.do_click(mouse_pos):
                        self.selected_input = choice
            else:
                for choice in self.choices:
                    if choice.do_click(mouse_pos):
                        self.selected_input = choice

        if self.selected_input:
            self.selected_input.selected = True

    def start(self):
        in_menu = True
        self.render()

        while in_menu:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return ['quit', ]

                if event.type == TEXTINPUT and self.selected_input:
                    self.selected_input.type(event)
                    self.render()

                if event.type == KEYDOWN and self.selected_input and not self.menu_display:
                    self.selected_input.special_type(event)
                    self.render()
                elif event.type == KEYDOWN and self.selected_input:
                    if event.key == K_BACKSPACE:
                        self.selected_input.delete()
                        self.render()

                elif event.type == KEYDOWN:
                    # Dans ce cas, nous appuyons sur une touche alors qu'aucun input n'est selectionné
                    if event.key == K_LSHIFT and not self.menu_display:  # shift for next scene by choice
                        self.displaying_next = not self.displaying_next
                        self.render()

                    if event.key == K_b and not self.menu_display:  # b for new choice
                        self.choices.append(
                            InputText(100, 100 * len(self.choices) + 5 * len(self.choices) + 100, 500, 40,
                                      background_color=(173, 173, 173, 128), outline=1,
                                      outline_color=(0, 0, 0), text_color=(255, 255, 255), selected=False))
                        self.next_choices.append(
                            InputText(100, 100 * len(self.next_choices) + 5 * len(self.next_choices) + 100, 500, 40,
                                      background_color=(173, 173, 173, 128), outline=1,
                                      outline_color=(0, 0, 0), text_color=(255, 255, 255), selected=False))
                        self.render()

                    if event.key == K_n and not self.menu_display:  # n pour "nouveau personnage"
                        menu = AskInfo(self.screen,
                                       "Tapez le chemin vers l'image du personnage à importer :\n(sans 'assets/')")
                        info = menu.start()
                        if info[0] == "quit":
                            return ["quit", ]
                        exist = False
                        while not exist:
                            if info[0] == "quit":
                                return ["quit", ]
                            elif not os.path.isfile("assets/" + info):
                                info = menu.start("L'image \"assets/" + info + "\" n'existe pas.")
                            else:
                                exist = True

                        # Maintenant qu'on a une image de personnage valide, on va l'ajouter à notre liste
                        self.characters.append({"image": "assets/" + info, "position": {"x": 0, "y": 0},
                                                "image_dev": pygame.image.load("assets/" + info)})
                    if event.key == K_BACKSPACE and not self.menu_display and self.dragged_char > -1:
                        # Permet de supprimer un personnage en appuyant sur le boutton supprimer lorsqu'on a une image selectionnée
                        self.characters.pop(self.dragged_char)
                        self.dragged_char = -1
                    if event.key == K_RETURN and not self.menu_display:
                        # Si on appuie sur Entrée, on enregistre la scène
                        # Pour cela, on crée le json de la scène point par point, puis on le renvoie
                        json_file = '{"type":"choice", "personnages":['
                        for char in self.characters:
                            json_file += '{"image":"' + char['image'] + '","position":{"x":' + str(char["position"]["x"]) + ',"y":' + str(char["position"]["y"]) +'}},'
                        if json_file[-1] == ',':
                            json_file = json_file[:len(json_file) - 1]
                        json_file += '],'
                        json_file += '"background":"' + self.background_input.get_value() + '",'
                        json_file += '"music":"' + self.music_input.get_value() + '",'
                        json_file += '"choices":['
                        for i in range(len(self.choices)):
                            json_file += '{"value":"' + self.choices[i].get_value() + '","next":"' + self.next_choices[i].get_value() + '"},'
                        if json_file[-1] == ',':
                            json_file = json_file[:len(json_file) - 1]
                        json_file += ']}'

                        return ["main_menu", json_file]

                    self.render()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.update_selected_input(pygame.mouse.get_pos())

                    if event.button == 2:
                        # On check d'abord si on touche une image
                        mouse_pos = pygame.mouse.get_pos()
                        for i in range(len(self.characters)):
                            if self.characters[i]["position"]["x"] <= mouse_pos[0] <= \
                                    self.characters[i]["image_dev"].get_size()[0] + self.characters[i]["position"]["x"]\
                                    and self.characters[i]["position"]["y"] <= mouse_pos[1] <= \
                                    self.characters[i]["image_dev"].get_size()[1] + self.characters[i]["position"]["y"]:
                                self.dragged_char = i
                                self.offset_drag[0] = mouse_pos[0] - self.characters[i]["position"]["x"]
                                self.offset_drag[1] = mouse_pos[1] - self.characters[i]["position"]["y"]

                    if event.button == 3:  # Clique droit
                        self.update_selected_input((-1, -1))  # On désélectionne notre input
                        self.menu_display = not self.menu_display  # Ouvre/Ferme le menu spécial
                        if not self.menu_display:
                            # On doit vérifier les changements sur background, pour en charger un autre si besoin
                            if os.path.isfile("assets/backgrounds/" + self.background_input.get_value()):
                                self.background = pygame.transform.scale(pygame.image.load("assets/backgrounds/" + self.background_input.get_value()), (1280, 720))
                            else:
                                self.background = None

                    self.render()
                if event.type == MOUSEBUTTONUP:
                    if event.button == 2:
                        self.dragged_char = -1  # On relache le drag
                if event.type == MOUSEMOTION:
                    if self.dragged_char > -1:
                        self.characters[self.dragged_char]["position"]["x"] = (pygame.mouse.get_pos()[0] - self.offset_drag[0])
                        self.characters[self.dragged_char]["position"]["y"] = (pygame.mouse.get_pos()[1] - self.offset_drag[1])
                        self.render()
