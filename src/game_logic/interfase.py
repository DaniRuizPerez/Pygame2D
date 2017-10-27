# -*- encoding: utf-8 -*-

import pygame, fase, endOfGame
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

class BotonSiguiente(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'contButton.png', (250, 550))
    def accion(self):
        self.pantalla.contenido.siguienteFase()

# -------------------------------------------------
# Clase TextoGUI y los distintos textos

class TextoSiguiente(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font("src/resources/fonts/gameFont.ttf", 42)
        TextoGUI.__init__(self, pantalla, fuente, (186, 0, 124), 'Siguiente fase', (300, 550))
    def accion(self):
        self.pantalla.contenido.siguienteFase()


# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class InterfaseGUI(PantallaGUI):
    def __init__(self, contenido):
        PantallaGUI.__init__(self, contenido, 'menu-background.png')
        import os
        pygame.mixer.music.load('src/resources/audio/drin_theme.mp3')
        pygame.mixer.music.play(-1)
        # Creamos los botones y los metemos en la lista
        botonSiguiente = BotonSiguiente(self)
        self.elementosGUI.append(botonSiguiente)
        # Creamos el texto y lo metemos en la lista
        textoSiguiente = TextoSiguiente(self)
        self.elementosGUI.append(textoSiguiente)


# -------------------------------------------------
# Clase MenuPygame, la escena en sí, en Pygame

class Interfase(EscenaPygame):

    def __init__(self, director, siguienteFaseId, estadisticasFinFase = None):
        # Llamamos al constructor de la clase padre
        EscenaPygame.__init__(self, director);
        # Creamos la lista de pantallas
        self.listaPantallas = []
        # Creamos las pantallas que vamos a tener
        #   y las metemos en la lista
        self.listaPantallas.append(InterfaseGUI(self))
        # En que pantalla estamos actualmente
        self.mostrarPantallaInicial()

        self.siguienteFaseId = siguienteFaseId
        self.estadisticasFinFase = estadisticasFinFase

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
        escena = fase.Fase(self.director, self.siguienteFaseId)
        self.director.cambiarEscena(escena)

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    # def mostrarPantallaConfiguracion(self):
    #    self.pantallaActual = ...


