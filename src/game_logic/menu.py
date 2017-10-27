# -*- encoding: utf-8 -*-

import pygame
from ..resources.pyganim import *
from pygame.locals import *
from escena import *
from ..resources.gestorRecursos import *
from fase import Fase
from ..resources.titleAnimations import *
from ..engines.elementoGUI import *
from ..engines.pantallaGUI import *
from ..engines.textoGUI import *
from ..engines.boton import *


# -------------------------------------------------
# Los distintos botones

class BotonJugar(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'startButton.png', (310, 422))
    def accion(self):
        self.pantalla.contenido.ejecutarJuego()

class BotonTienda(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'storButton.png', (335, 470))
    def accion(self):
        self.pantalla.contenido.entrarTienda()

class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'exitButton.png', (310, 516))
    def accion(self):
        self.pantalla.contenido.salirPrograma()

class BotonNivel(Boton):
	def __init__(self, pantalla, nivel):
		self.nivel = nivel
		self.clicked = False
		Boton.__init__(self, pantalla, 'levelButton'+ str(nivel) +'.png', (300 + (nivel-1)*20, (((nivel-1)%2)*30) + 575))
		self.imagen = pygame.transform.scale(self.imagen, (35, 35))
		self.imagen.set_alpha(100)

	def accion(self):
		if self.clicked == False:
			self.setClicked(True)
		else:
			self.setClicked(False)
		self.pantalla.contenido.cambiarNivel(self.nivel)

	def isClicked(self):
		return self.clicked

	def setClicked(self, clicked):
		if clicked == False:
			self.imagen.set_alpha(100)
		else:
			self.imagen.set_alpha(255)
		self.clicked = clicked

# -------------------------------------------------
# Los distintos textos

class TextoJugar(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font("src/resources/fonts/gameFont.ttf", 42)
        TextoGUI.__init__(self, pantalla, fuente, (186, 0, 124), 'Jugar', (370, 422))
    def accion(self):
        self.pantalla.contenido.ejecutarJuego()

class TextoTienda(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font("src/resources/fonts/gameFont.ttf", 42)
        TextoGUI.__init__(self, pantalla, fuente, (186, 0, 124), 'Tienda', (395, 470))
    def accion(self):
        self.pantalla.contenido.entrarTienda()


class TextoSalir(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font("src/resources/fonts/gameFont.ttf", 42)
        TextoGUI.__init__(self, pantalla, fuente, (186, 0, 124), 'Salir', (370, 516))
    def accion(self):
        self.pantalla.contenido.salirPrograma()

# -------------------------------------------------
# Las distintas pantallas

class PantallaInicialGUI(PantallaGUI):
    def __init__(self, contenido):
        PantallaGUI.__init__(self, contenido, 'menu-background.png')
        pygame.mixer.music.load('src/resources/audio/drin_theme.mp3')
        pygame.mixer.music.play(-1)
        # Creamos los botones y los metemos en la lista
        botonJugar = BotonJugar(self)
        botonTienda = BotonTienda(self)
        botonSalir = BotonSalir(self)
        niveles = []
        self.botonesNivel = []

        self.elementosGUI.append(botonJugar)
        self.elementosGUI.append(botonTienda)
        self.elementosGUI.append(botonSalir)
        for x in xrange(1,11):
        	niveles.append(BotonNivel(self, x))
        	self.botonesNivel.append(niveles[x-1])
        niveles[0].setClicked(True)
        
        # Creamos el texto y lo metemos en la lista
        textoJugar = TextoJugar(self)
        textoTienda = TextoTienda(self)
        textoSalir = TextoSalir(self)
        self.elementosGUI.append(textoJugar)
        self.elementosGUI.append(textoTienda)
        self.elementosGUI.append(textoSalir)

        animacionTitulo = AnimacionTitulo()
        animacionTitulo.scale((340,178))
        animacionTitulo.posicionx = 230
        animacionTitulo.posiciony = 10
        animacionTitulo.play()
        self.animaciones.append(animacionTitulo)

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == MOUSEBUTTONDOWN:
                self.elementoClic = None
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        self.elementoClic = elemento
                for botonNivel in self.botonesNivel:
                    if botonNivel.posicionEnElemento(evento.pos):
                        self.elementoClic = botonNivel
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if (elemento == self.elementoClic):
                            elemento.accion()
                for botonNivel in self.botonesNivel:
                    botonNivel.setClicked(False)
                    if botonNivel.posicionEnElemento(evento.pos):
                        if (botonNivel == self.elementoClic):
                            botonNivel.accion()

    def dibujar(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        # Después las animaciones
        for animacion in self.animaciones:
            animacion.dibujar(pantalla)
        # Después los botones
        for elemento in self.elementosGUI:
            elemento.dibujar(pantalla)

        for botonNivel in self.botonesNivel:
            botonNivel.dibujar(pantalla)


       

# -------------------------------------------------
# Clase MenuPygame, la escena en sí, en Pygame

class Menu(EscenaPygame):

    def __init__(self, director):
        # Llamamos al constructor de la clase padre
        EscenaPygame.__init__(self, director);
        # Creamos la lista de pantallas
        self.listaPantallas = []
        # Creamos las pantallas que vamos a tener
        #   y las metemos en la lista
        self.listaPantallas.append(PantallaInicialGUI(self))
        # En que pantalla estamos actualmente
        self.mostrarPantallaInicial()
        self.nivelFase = 1

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
    # Metodos propios del menu

    def cambiarNivel(self, nivel):
    	self.nivelFase = nivel #Cuando se crea la fase se recoge el valor de nivelFase
        self.director.setDificultyLevel(nivel)

    def salirPrograma(self):
        self.director.salirPrograma()

    def entrarTienda(self):
        '''LOL NOPE YET'''

    def ejecutarJuego(self):
        # Creamos la escena con la animacion antes de jugar
        pygame.mixer.music.stop()
        escena = Fase(self.director, 'fase1Oleada1')
        self.director.apilarEscena(escena)

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    # def mostrarPantallaConfiguracion(self):
    #    self.pantallaActual = ...


