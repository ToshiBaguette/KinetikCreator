import io
import json
import pygame
import os
import MainMenu
import AskInfo
import EditScene


def init():
    """Fonction d'initialisation de l'application"""

    # D'abord on vérifie l'existence de tous les répertoires utiles
    repertories = ["scenes", "assets", "saves", "assets/backgrounds", "assets/musics"]
    for rep in repertories:
        if not os.path.isdir(rep):
            os.mkdir(rep)

    # Ensuite on construit notre fenêtre pygame
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    return screen


def start(screen):
    """Fonction s'occupant rapidement de la boucle de jeu"""
    state = ["main_menu"]
    in_game = True
    while in_game:
        if state[0] == "quit":
            in_game = False
        elif state[0] == "main_menu":
            menu = MainMenu.MainMenu(screen)
            state = menu.start()

        elif state[0] == "create_scene":  # Quand on clique sur "Nouvelle scène", on doit taper un nom
            # Si la scène existe déjà, on l'édit aussi
            menu = AskInfo.AskInfo(screen, "Entrez un nom de scène :")
            info = menu.start()
            if info[0] == "quit":
                return ["quit", ]
            if not os.path.isfile("scenes/scene_" + info + ".json"):
                file = open("scenes/scene_" + info + ".json", "w")
                file.write('{"personnage": [], "flags": [], "events": [], "background": "", "text": "", "next":""}')  # On enregistre un JSON presque vide
                file.close()
            state = ["edit_scene", info]

        elif state[0] == "choose_scene":  # Quand on clique sur "Ouvrir un scène", on doit taper laquelle on veut modif
            menu = AskInfo.AskInfo(screen, "Entrez le nom de la scène à modifier :")
            exist = False
            info = menu.start()
            if info[0] == "quit":
                return ["quit", ]
            while not exist:  # Check si la scène existe ou non
                if info[0] == "quit":
                    return ["quit", ]
                elif not os.path.isfile("scenes/scene_" + info + ".json"):
                    info = menu.start("La scène numéro " + info + " n'existe pas.")
                else:
                    exist = True
            state = ["edit_scene", info]

        elif state[0] == "edit_scene":  # Une fois que le nom de scène a été choisi
            # On doit commencer par récupérer le json
            name_scene = "scenes/scene_" + state[1] + ".json"
            file_scene = io.open(name_scene, 'r', encoding='utf-8')
            json_scene = json.load(file_scene)
            file_scene.close()
            menu = EditScene.EditScene(screen, json_scene)
            state = menu.start()

            if len(state) > 1:
                # Ici, on a reçu un json à enregistrer
                file_scene = io.open(name_scene, 'w', encoding='utf-8')
                file_scene.write(state[1])
                file_scene.close()


if __name__ == "__main__":
    screen = init()
    start(screen)
    pygame.quit()
