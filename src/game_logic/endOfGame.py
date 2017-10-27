# -*- encoding: utf-8 -*-

import pygame, fase
from ..resources.pyganim import *
from pygame.locals import *
from escena import *
from ..resources.gestorRecursos import *
from ..resources.titleAnimations import *

from ..engines.pantallaGUI import *
from ..engines.textoGUI import *
from ..engines.boton import *



# -------------------------------------------------
# Clase Boton y los distintos botones

class BotonVolverAlMenu(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'contButton.png', (250, 550))
    def accion(self):
        self.pantalla.contenido.siguienteFase()

# -------------------------------------------------
# Clase TextoGUI y los distintos textos

class TextoVolverAlMenu(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font("src/resources/fonts/gameFont.ttf", 42)
        TextoGUI.__init__(self, pantalla, fuente, (186, 0, 124), 'Volver al menu', (300, 550))
    def accion(self):
        self.pantalla.contenido.siguienteFase()

class TextoCongratulations(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font("src/resources/fonts/gameFont.ttf", 60)
        TextoGUI.__init__(self, pantalla, fuente, (186, 0, 124), 'CONGRATULATIONS!!!', (150, 100))
    def accion(self):
        return

class TextoGameOver(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font("src/resources/fonts/gameFont.ttf", 60)
        TextoGUI.__init__(self, pantalla, fuente, (186, 0, 124), 'TAT GAME OVER TAT', (150, 100))
    def accion(self):
        return


# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class EndOfGameGUI(PantallaGUI):
    def __init__(self, contenido):
        PantallaGUI.__init__(self, contenido, 'menu-background.png')
        import os
        pygame.mixer.music.load('src/resources/audio/drin_theme.mp3')
        pygame.mixer.music.play(-1)
        if (contenido.isSucceded()):
            self.elementosGUI.append(TextoCongratulations(self))
        else:
            self.elementosGUI.append(TextoGameOver(self))
        # Creamos los botones y los metemos en la lista
        self.elementosGUI.append(BotonVolverAlMenu(self))
        # Creamos el texto y lo metemos en la lista
        self.elementosGUI.append(TextoVolverAlMenu(self))


# -------------------------------------------------
# la escena en sí, en Pygame

class EndOfGame(EscenaPygame):
    def __init__(self, director, succed, estadisticasFinFase = None):
        # Llamamos al constructor de la clase padre
        EscenaPygame.__init__(self, director);
        # Creamos la lista de pantallas
        self.listaPantallas = []
        self.succed = succed
        # Creamos las pantallas que vamos a tener
        #   y las metemos en la lista
        self.listaPantallas.append(EndOfGameGUI(self))
        # En que pantalla estamos actualmente
        self.mostrarPantallaInicial()

        self.estadisticasFinFase = estadisticasFinFase

    def isSucceded(self):
        return self.succed

    def update(self, *args):
        return

    def eventos(self, lista_eventos):
        # Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    self.salirPrograma()
            elif evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)

    #--------------------------------------

    def siguienteFase(self):
        pygame.mixer.music.stop()
        self.director.salirEscena()

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    # def mostrarPantallaConfiguracion(self):
    #    self.pantallaActual = ...
