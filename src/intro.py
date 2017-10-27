# -*- encoding: utf-8 -*-

import pyglet
import random

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

VELOCIDAD_TIERRA = 0.1 # Escala por segundo
VELOCIDAD_ALFA_MALAN = 35 # Opacidad por segundo
VELOCIDAD_ESCALA_DRIN = 0.2 # Escala por segundo

# Funcion auxiliar que crea una animacion a partir de una imagen que contiene la animacion
#  dividida en filas y columnas
def crearFramesAnimacion(nombreImagen, filas, columnas):
    # Cargamos la secuencia de imagenes del archivo
    secuenciaImagenes = pyglet.image.ImageGrid(pyglet.image.load(nombreImagen), filas, columnas)
    # Creamos la secuencia de frames
    secuenciaFrames = []
    # Para cada fila, del final al principio
    for fila in range(filas, 0, -1):
        end = fila * columnas
        start = end - (columnas -1) -1
        # Para cada imagen de la fila
        for imagen in secuenciaImagenes[start:end:1]:
            # Creamos un frame con esa imagen, indicandole que tendra una duracion de 0.5 segundos
            frame = pyglet.image.AnimationFrame(imagen, 0.1)
            #  y la anadimos a la secuencia de frames
            secuenciaFrames.append(frame)

    # Devolvemos la secuencia de frames
    return secuenciaFrames




# -------------------------------------------------
# Clase para las animaciones que solo ocurriran una vez
#  (sin bucles)

class Animacion(pyglet.window.Window):

    def __init__(self):
        # Constructores de la clase padre
        pyglet.window.Window.__init__(self, ANCHO_PANTALLA, ALTO_PANTALLA)

        self.splashDRIN = None
        self.splashMalanDRIN = None
        self.titulo = None
        self.DRIN = False
        self.malanDRIN = False

        # La imagen de fondo
        self.imagen = pyglet.image.load('resources/imagenes/intro-background.png')
        self.imagen = pyglet.sprite.Sprite(self.imagen)
        self.imagen.scale = float(ANCHO_PANTALLA) / self.imagen.width

        # Registramos que se actualice una vez por frame
        pyglet.clock.schedule(self.update)

        # Las animaciones que habra en esta escena
        # No se crean aqui las animaciones en si, porque se empiezan a reproducir cuando se crean
        # Lo que se hace es cargar los frames de disco para que cuando se creen ya esten en memoria

        # Creamos el batch de las animaciones
        self.batch = pyglet.graphics.Batch()
        # Y los grupos para ponerlas por pantalla
        self.grupoDetras =  pyglet.graphics.OrderedGroup(0)
        self.grupoMedio =   pyglet.graphics.OrderedGroup(1)
        self.grupoDelante = pyglet.graphics.OrderedGroup(2)


        # La animacion del tanque la creamos a partir de un gif animado
        self.earth = pyglet.sprite.Sprite(pyglet.resource.animation('resources/imagenes/earthSpin.gif'), batch=self.batch, group=self.grupoDetras)
        # Esta si que se crea porque estara desde el principio
        self.earth.scale = 0.1
        self.earth.set_position(ANCHO_PANTALLA/2 - self.earth.width/2, ALTO_PANTALLA/2 - self.earth.height/2)

        pyglet.clock.schedule_once(self.aparecerTitulo, 8)
        pyglet.clock.schedule_once(self.aparecerDRIN, 1)
        pyglet.clock.schedule_once(self.aparecerMalanDRIN, 3)
        

    # El metodo para eliminar una animacion determinada
    def eliminarAnimacion(self, tiempo, animacion):
        animacion.delete()

    # Metodo que hace aparecer una animacion de humo en el cielo
    def aparecerDRIN(self, tiempo):
        self.splashDRIN = pyglet.sprite.Sprite(pyglet.resource.image('resources/imagenes/drinSplashIntro.png'), batch=self.batch, group=self.grupoMedio)
        self.splashDRIN.scale = 0.2
        self.splashDRIN.set_position(0 - self.splashDRIN.width, 0 - self.splashDRIN.height/2)
        self.DRIN = True


    # Metodo para hacer aparecer la animacion del humo en el tanque
    def aparecerMalanDRIN(self, tiempo):
        self.splashMalanDRIN = pyglet.sprite.Sprite(pyglet.resource.image('resources/imagenes/malandrinSplash.png'), batch=self.batch, group=self.grupoMedio)
        self.splashMalanDRIN.opacity = 0
        self.splashMalanDRIN.scale = 0.75
        self.splashMalanDRIN.set_position(ANCHO_PANTALLA/2 - self.splashMalanDRIN.width/8, ALTO_PANTALLA/2 - self.splashMalanDRIN.height/2)
        self.malanDRIN = True

    # Metodo para hacer aparecer la animacion de la explosion en el tanque
    def aparecerTitulo(self, tiempo):
        # Creamos la animacion de la explosion
        self.titulo = pyglet.sprite.Sprite(pyglet.resource.animation('resources/imagenes/tituloSplash.gif'), batch=self.batch, group=self.grupoDelante)
        self.titulo.scale = 0.75
        self.titulo.set_position(ANCHO_PANTALLA/2 - self.titulo.width/2, ALTO_PANTALLA - self.titulo.height - 20)



    
    # El evento relativo a la pulsacion de una tecla
    def on_key_press(self, symbol, modifiers):
        # Si se pulsa Escape, se sale de la animacion
        self.close()


    # El evento que se ejecuta cada vez que hay que dibujar la pantalla
    def on_draw(self):
        # Si la ventana esta visible
        if self.visible:
            # Borramos lo que hay en pantalla
            self.clear()
            # Dibujamos la imagen
            if self.imagen!=None:
                self.imagen.draw()
            # Y, para cada animacion, la dibujamos
            # Para hacer esto, le decimos al batch que se dibuje
            self.batch.draw()


    # El evento relativo al clic del raton
    def on_mouse_press(self, x, y, button, modifiers):
        # Si se pulsa el boton izquierdo
        if (pyglet.window.mouse.LEFT == button):
            self.close()


    # El evento que sera llamado periodicamente
    def update(self, tiempo):
        if self.earth.scale < 0.8:
            self.earth.scale = self.earth.scale + tiempo*VELOCIDAD_TIERRA
            self.earth.set_position(ANCHO_PANTALLA/2 - self.earth.width/2, ALTO_PANTALLA/2 - self.earth.height/2)

        if self.DRIN:
            if self.splashDRIN.scale < 0.6:
                self.splashDRIN.scale = self.splashDRIN.scale + tiempo*VELOCIDAD_ESCALA_DRIN
            else:
                self.DRIN = False

        if self.malanDRIN:
            if self.splashMalanDRIN.opacity < 200:
                self.splashMalanDRIN.opacity = self.splashMalanDRIN.opacity + tiempo*VELOCIDAD_ALFA_MALAN
            else:
                self.malanDRIN = False

if __name__ == '__main__':

    animacion = Animacion()

    # Ejecutamos la aplicacion de pyglet
    pyglet.app.run()

