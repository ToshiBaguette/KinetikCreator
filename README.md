This project is only useful for my other project: UniverseGenesis => https://github.com/Toshibane/UniverseGenesis.

As UniverseGenesis is a Visual Novel Reader, KinetikCreator is the software allowing to create the scenes that will be read by UniverseGenesis.
It is fully written in Python with Pygame as a sole dependency.

## HOW IT WORKS

First, there's a main menu, allowing to choose between creating a new scene, or editing an existing one.

While editing, you can click on the center textbox to start typing the text for the scene. 

Then, you can right click anywhere on the window to access the configuration of the scene. Here, you can change the background and the music of the scene.

The background must only be a filename (with the extension), and the file must be present in `assets/backgrounds`, as the music must only be a filename too and must be present in `assets/musics`.

While on the primary screen, for editing the scene, you can press the `N` key, and enter the path from assets to an image, to add it to the scene. With a click of the wheel on an image, and by moving the mouse as you hold your click, you can freely move the images.

Finally, by pressing enter while nothing is selected, you can save the scene.

## CODE BASICS

Every menu in the game has its own class, with some basic functions as render make it visible, and start to open the menu.

Then, there are three items created for UI : KineticButton and InputText.

KineticButton is a button, with a render function, and basic functions to change the text, get the value or handle the hover functionality.

InputText is a textbox where you can type text, with a basic implementation of a cursor in the text.

Finally, there is a `utils.py` file, containing useful functions such as the loading and saving of the scenes.