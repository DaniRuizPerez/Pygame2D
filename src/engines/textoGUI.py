# -*- encoding: utf-8 -*-

from elementoGUI import *

# -------------------------------------------------
# Clase TextoGUI 

class TextoGUI(ElementoGUI):
    def __init__(self, pantalla, fuente, color, texto, posicion):
        # Se crea la imagen del texto
        self.imagen = fuente.render(texto, True, color)
        self.color = color
        self.fuente = fuente
        self.posicion = posicion
        # Se llama al método de la clase padre con el rectángulo que ocupa el texto
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def updateText(self, texto):
    	self.imagen = self.fuente.render(texto, True, self.color)
    	self.rect = self.imagen.get_rect()
    	self.establecerPosicion(self.posicion)