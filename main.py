# -*- coding: utf-8 -*-

# Importar modulos
from src.actors.drin import *
from src.game_logic.director import *
from src.game_logic.menu import *
import glob, os


if __name__ == '__main__':
    # Creamos el director
    director = Director()
    # Creamos la escena con el menu
    escena = Menu(director)
    # Le decimos al director que apile esta escena
    director.apilarEscena(escena)
    # Creamos al personaje jugable
    director.setDr1n(DRIN(escena))
    # Y ejecutamos el juego
    director.ejecutar()

    '''Clean .pyc annoying files'''
    path = '.'
    for root, dirs, files in os.walk(path):
        for currentFile in files:
            ext='.pyc'
            if currentFile.lower().endswith(ext):
                os.remove(os.path.join(root, currentFile))