import io
import json
import pygame
import os
import MainMenu
import AskInfo
import EditScene
import utils
from NewSceneAsk import NewSceneAsk
from EditChoice import EditChoice


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
            menu = NewSceneAsk(screen)
            info = menu.start()

            if info[0] == "quit":
                return ["quit", ]

            if not os.path.isfile("scenes/scene_" + info[0] + ".json"):
                empty_json = ""
                if info[1]:
                    empty_json = '{"type": "choice", "personnages":[], "background": "", "music":"", "choices":[]}'
                else:
                    empty_json = '{"type":"scene", "personnages": [], "flags": [], "events": [], "background": "", "music":"", "text": "", "next":""}'
                utils.save_scene(empty_json, info[0])

            state = ["edit_scene", info[0]]

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
                    info = menu.start("La scène " + info + " n'existe pas.")
                else:
                    exist = True
            state = ["edit_scene", info]

        elif state[0] == "edit_scene":  # Une fois que le nom de scène a été choisi
            # On doit commencer par récupérer le json
            name_scene = str(state[1])

            json_scene = utils.load_scene(name_scene)

            menu = None
            if json_scene["type"] == "choice":
                menu = EditChoice(screen, json_scene)
            else:
                menu = EditScene.EditScene(screen, json_scene)

            state = menu.start()

            if len(state) > 1:
                # Ici, on a reçu un json à enregistrer
                utils.save_scene(state[1], name_scene)

                # On demande un nom, pour commencer directement la prochaine save
                menu = AskInfo.AskInfo(screen, "Nom de la prochaine scene :")
                next_scene_name = menu.start()
                if next_scene_name[0] != "quit":
                    # On enregistre directement le champs next de l'ancienne scene
                    json_old = json.loads(state[1])
                    json_old["next"] = next_scene_name
                    utils.save_scene(json.dumps(json_old), name_scene)

                    if not os.path.isfile("scenes/scene_" + next_scene_name + ".json"):
                        # Pour gagner du temps, on reprend le même background, et la même musique que pour la scène précédente
                        # Il y a de grandes chances que ces deux attributs ne changent pas d'une scène à l'autre
                        new_json = '{"personnages": [], "flags": [], "events": [], "background": "' + json_old["background"] + '", "music":"' + json_old["music"] + '", "text": "", "next":""}'
                        utils.save_scene(new_json, next_scene_name)
                    state = ["edit_scene", next_scene_name]
                else:
                    return ['quit', ]


if __name__ == "__main__":
    screen = init()
    start(screen)
    pygame.quit()
