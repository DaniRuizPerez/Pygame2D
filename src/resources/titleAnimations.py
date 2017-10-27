# -*- encoding: utf-8 -*-

import pyganim

# Extendemos la clase animacion de PygAnimation para darle posicion
class Animacion(pyganim.PygAnimation):
    def __init__(self, *args):
        pyganim.PygAnimation.__init__(self, args)
        # Posicion que tendra esta animacion
        self.posicionx = 0
        self.posiciony = 0
        
    def mover(self, distanciax, distanciay):
        self.posicionx += distanciax
        self.posiciony += distanciay

    def dibujar(self, pantalla):
        self.blit(pantalla, (self.posicionx, self.posiciony))

# Las distintas animaciones que tendremos

# La animacion del fuego
class AnimacionTitulo(Animacion):
    def __init__(self):
        pyganim.PygAnimation.__init__(self,[
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-001.png', 3),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-002.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-003.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-004.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-005.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-006.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-007.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-008.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-009.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-010.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-011.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-012.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-013.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-002.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-003.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-004.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-005.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-006.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-007.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-008.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-009.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-010.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-011.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-012.png', 0.05),
                                        ('src/resources/imagenes/tituloAnim/tituloSplash-013.png', 0.05)])
