# -*- encoding: utf-8 -*-

import pygame
from elementoGUI import *
from ..resources.pyganim import *
from ..resources.constants import *
from ..resources.gestorRecursos import *


# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class PantallaGUI:
    def __init__(self, contenido, nombreImagen):
        self.contenido = contenido
        # Se carga la imagen de fondo
        self.imagen = GestorRecursos.CargarImagen(nombreImagen)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        # Se tiene una lista de elementos GUI
        self.elementosGUI = []
        # Se tiene una lista de animaciones
        self.animaciones = []

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == MOUSEBUTTONDOWN:
                self.elementoClic = None
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        self.elementoClic = elemento
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if (elemento == self.elementoClic):
                            elemento.accion()

    def dibujar(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        # Después las animaciones
        for animacion in self.animaciones:
            animacion.dibujar(pantalla)
        # Después los botones
        for elemento in self.elementosGUI:
            elemento.dibujar(pantalla)