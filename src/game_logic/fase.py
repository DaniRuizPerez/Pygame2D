# -*- coding: utf-8 -*-

import pygame, escena
from interfase import *
from endOfGame import *
from ..game_logic.escena import *
from ..actors.actor import *
from ..resources.constants import *
from pygame.locals import *
from ..actors.drin import *
from ..actors.platform import *
from ..actors.floor import *
from ..actors.trap import *
from ..actors.void import *
from ..actors.cactus import *
from ..actors.scorpion import *
from ..actors.camel import *
from ..actors.penguin import *
from ..actors.snowman import *
from ..actors.jetty import *
from ..actors.respawn import *

from ..engines.textoGUI import *
from ..engines.boton import *
# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

VELOCIDAD_SOL = 0.1 # Pixeles por milisegundo

# Los bordes de la pantalla para hacer scroll horizontal
MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

# -------------------------------------------------
# Clase Fase

class Fase(EscenaPygame):
    def __init__(self, director, faseId):

        #Inicializamos los grupos
        EscenaPygame.__init__(self, director)

        #Cogemos la definicion de la fase del gestor de recursos
        root = GestorRecursos.CargarFase(faseId)

        #Inicializamos los grupos
        self.createGroups()
        self.time = 0

        # Creamos el decorado y el fondo
        self.large = int(root.find('large').text)
        if self.large < ANCHO_PANTALLA:
            self.large = ANCHO_PANTALLA

        # Establecemos la dificultad de la fase
        self.setLevel(director.getDificultyLevel())
       	self.hdMode = False

        # Guardamos cual sera la siguiente fase en caso de exito
        try:
            self.nextPhase = root.find( 'nextPhase' ).text
            if (self.nextPhase == 'menu' or self.nextPhase == 'none' or self.nextPhase == ''):
                self.nextPhase = None
        except AttributeError:
            self.nextPhase = None

        self.decorado = Decorado(root.find('background').text, self.large)
        self.fondo = Cielo(root.find('sky').text)
        self.scrollx = 0

        self.createVoid(self.large) 

        if (root.find('background').text == 'dessertBack'):
            pygame.mixer.music.load('src/resources/audio/desert.mp3')
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.load('src/resources/audio/ice.mp3')
            pygame.mixer.music.play(-1)


        # Creamos las plataformas
        for element in root.find( 'platfotms' ).findall( 'platform' ):
            platX = int(element.find( 'position' ).get( 'x' ))
            platY = int(element.find( 'position' ).get( 'y' ))
            platSize = int(element.find( 'size' ).text)
            platImage = element.find('image').text
            self.createPlatform(platX, platY, platSize, platImage)

        # Creamos las trampas
        for element in root.find( 'traps' ).findall( 'trap' ):
            x = int(element.get( 'x' ))
            y = int(element.get( 'y' ))
            self.createTrap(x, y, element.text)

        # Despues, para que queden por encima, las plataformas del suelo
        for element in root.find( 'floor' ).findall( 'surface' ):
            x = int(element.get( 'position' ))
            length = int(element.get( 'length' ))
            self.createFloor(x, length, element.text)


        self.respawn = Respawn(self.large, self)
        # Creamos a los enemigos
        for element in root.find( 'enemies' ).findall( 'enemy' ):
            enemyType = element.find( 'type' ).text
            quantity = int(element.find( 'quantity' ).text)
            maxActive = int(element.find( 'maxActive' ).text)
            minWait = int(element.find( 'minWait' ).text)
            self.respawn.add(enemyType, quantity, maxActive, minWait)

        self.textoEnemiesRemaining = TextoEnemiesRemaining(self, self.respawn.enemiesRemaining())
        self.createPlayer((self.large/2, 50))


    def setLevel(self, lvl):
        self.level = lvl

    def getLevel(self):
        return self.level

    def getGrupoTraps (self):
        return self.grupoTraps

    def enemyKilled(self, enemyType):
        self.respawn.enemyKilled(enemyType)
        
    def createPlayer(self, position):
        self.drin = self.director.getDr1n()
        self.drin.completlyHeal()
        self.drin.physics.fixPosition(position)
        self.registerPlayer(self.drin)

        self.botonVida = BotonVida(self)
        self.textoVida = TextoVida(self, self.drin.getActualHP())

    def createPlatform(self, minx, miny, size, image):
        altura = ALTO_PANTALLA - miny - 30

        if (size < 60):
            self.createPlatformSegment(minx,         miny, size,      15, False, image + 'Top')
            self.createPlatformSegment(minx,         miny+15, size,   altura, True, image + 'Fill')
        else:
            self.createPlatformSegment(minx,            miny, 20,           15, False, image + 'TopLeft')
            self.createPlatformSegment(minx+20,         miny, size-40,      15, False, image + 'Top')
            self.createPlatformSegment(minx+size-20,    miny, 20,           15, False, image + 'TopRight')

            self.createPlatformSegment(minx,            miny+15, 20,        altura, True, image + 'Left')
            self.createPlatformSegment(minx+20,         miny+15, size-40,   altura, True, image + 'Fill')
            self.createPlatformSegment(minx+size-20,    miny+15, 20,        altura, True, image + 'Right')

    def createPlatformSegment(self, minx, miny, deltax, deltay, fill, image):
        img = GestorRecursos.GetImageFileName(image)
        plat = Platform((minx, miny, deltax, deltay), img, self)
        self.registerStaticPlatform(plat, fill)

    def createFloor(self, x, length, image):
        if (length < 60):
            self.createFloorSegment(x,         length,    False, image + 'Top')
            self.createFloorSegment(x,         length,    True, image + 'Fill')
        else:
            self.createFloorSegment(x,            20,           False, image + 'TopLeft')
            self.createFloorSegment(x+20,         length-40,    False, image + 'Top')
            self.createFloorSegment(x+length-20,  20,           False, image + 'TopRight')

            self.createFloorSegment(x,            20,           True, image + 'Left')
            self.createFloorSegment(x+20,         length-40,    True, image + 'Fill')
            self.createFloorSegment(x+length-20,  20,           True, image + 'Right')

    def createFloorSegment(self, x, length, fill, image):
        img = GestorRecursos.GetImageFileName(image)
        plat = Floor(x, length, fill, img, self)
        self.registerFloor(plat, fill)

    def createTrap(self, x, y, image):
        img = GestorRecursos.GetImageFileName(image)
        plat = Trap(x, y, img, self)
        self.registerTrap(plat)

    def createVoid(self,length):
        plat = Void(length, self)
        self.registerVoid(plat)

    def createEnemy(self, enemyType, pos):
        if enemyType == 'cactus':
            self.createCactus(pos)
        elif enemyType == 'scorpion':
            self.createScorpion(pos)
        elif enemyType == 'camel':
            self.createCamel(pos)
        elif enemyType == 'penguin':
            self.createPenguin(pos)
        elif enemyType == 'snowman':
            self.createSnowman(pos)
        elif enemyType == 'jetty':
            self.createJetty(pos)

    def createCactus (self, pos):
        enemy = Cactus(self)
        enemy.physics.fixPosition(pos)
        self.registerEnemy(enemy)

    def createScorpion (self, pos):
        enemy = Scorpion(self)
        enemy.physics.fixPosition(pos)
        self.registerEnemy(enemy)

    def createCamel (self, pos):
        enemy = Camel(self)
        enemy.physics.fixPosition(pos)
        self.registerEnemy(enemy)

    def createPenguin (self, pos):
        enemy = Penguin(self)
        enemy.physics.fixPosition(pos)
        self.registerEnemy(enemy)

    def createSnowman (self, pos):
        enemy = Snowman(self)
        enemy.physics.fixPosition(pos)
        self.registerEnemy(enemy)

    def createJetty (self, pos):
        enemy = Jetty(self)
        enemy.physics.fixPosition(pos)
        self.registerEnemy(enemy)

    def createGroups(self):
        self.grupoSprites = pygame.sprite.Group()
        self.grupoSpritesDinamicos = pygame.sprite.Group()

        self.grupoEnemigos = pygame.sprite.Group()

        self.grupoJugadores = pygame.sprite.Group()

        self.grupoPlatformsFill = pygame.sprite.Group()
        self.grupoPlatforms = pygame.sprite.Group()
        self.grupoTraps = pygame.sprite.Group()
        self.grupoFloorFill = pygame.sprite.Group()
        self.grupoFloor = pygame.sprite.Group()
        self.grupoVoid = pygame.sprite.Group()

        self.grupoDisparosJugador = pygame.sprite.Group()
        self.grupoGolpesJugador = pygame.sprite.Group()

        self.grupoDisparosEnemigo = pygame.sprite.Group()
        self.grupoGolpesEnemigo = pygame.sprite.Group()
        

    def getPlayerShots(self):
        return self.grupoDisparosJugador
        

    def registerSprite(self, sprite):
        self.grupoSprites.add(sprite)

    def registerDynamicSprite(self, dSprite):
        self.grupoSpritesDinamicos.add(dSprite)
        self.grupoSprites.add(dSprite)

    def registerEnemy(self, sprite):
        self.grupoEnemigos.add(sprite)
        self.registerDynamicSprite(sprite)

    def registerPlayer(self, sprite):
        self.grupoJugadores.add(sprite)
        self.registerDynamicSprite(sprite)

    def registerStaticPlatform(self, platform, fill):
        if fill:
            self.grupoPlatformsFill.add(platform)
        else:
            self.grupoPlatforms.add(platform)
        self.registerSprite(platform)

    def registerFloor(self, platform, fill):
        if fill:
            self.grupoFloorFill.add(platform)
        else:
            self.grupoFloor.add(platform)
        self.registerSprite(platform)

    def registerVoid(self, platform):
        self.grupoFloor.add(platform)
        self.grupoVoid.add(platform)
        self.registerSprite(platform)

    def registerTrap(self, platform):
        self.grupoTraps.add(platform)
        self.registerSprite(platform)

    def registerDynamicPlatform(self, platform):
        self.grupoPlatforms.add(platform)
        self.registerDynamicSprite(platform)

    def registerEnemyShot(self, shot):
        self.grupoDisparosEnemigo.add(shot)
        self.registerDynamicSprite(shot)

    def registerPlayerShot(self, shot):
        self.grupoDisparosJugador.add(shot)
        self.registerDynamicSprite(shot)

    def registerEnemyHit(self, shot):
        self.grupoGolpesEnemigo.add(shot)
        self.registerDynamicSprite(shot)

    def registerPlayerHit(self, shot):
        self.grupoGolpesJugador.add(shot)
        self.registerDynamicSprite(shot)

        
    # Devuelve True o False según se ha tenido que desplazar el scroll
    def actualizarScrollOrdenados(self, jugador):
        #Si el jugador se sale por la izquierda
        if (jugador.rect.left<=MINIMO_X_JUGADOR):
            #Si esta en el limite izquierdo del scroll, no se puede hacer mas
            #Se le pone en el limite por si se ha pasado
            if (self.scrollx <= 0):
                jugador.physics.fixPosition((MINIMO_X_JUGADOR , jugador.physics.getPosition()[1]))
                self.scrollx = 0
                return True; 
            else:
                #Si se puede desplazar el escenario, se devuelve true y se cambia el scroll
                desplazamiento = MINIMO_X_JUGADOR - jugador.rect.left
                self.scrollx = self.scrollx - desplazamiento;
                return True; 

        if (jugador.rect.right>=MAXIMO_X_JUGADOR):
            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = jugador.rect.right - MAXIMO_X_JUGADOR
            # Si el escenario ya está a la derecha del todo, no lo movemos mas
            if self.scrollx + ANCHO_PANTALLA >= self.decorado.rect.right:
                self.scrollx = self.decorado.rect.right - ANCHO_PANTALLA
                # En su lugar, colocamos al jugador que esté más a la derecha a la derecha de todo
                jugador.physics.fixPosition((self.scrollx+MAXIMO_X_JUGADOR-jugador.rect.width, jugador.physics.getPosition()[1]))
                return True; # No se ha actualizado el scroll
           
            else:
                #Si se puede desplazar el escenario, se devuelve true y se cambia el scroll
                self.scrollx = self.scrollx + desplazamiento;
                return True; 

        return False;


    def actualizarScroll(self, drin):
        #se mira si hay que actualizar el scroll
        cambioScroll = self.actualizarScrollOrdenados(drin)

        # Si se cambio el scroll, se desplazan todos los Sprites y el decorado
        if cambioScroll:
            # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
            for sprite in iter(self.grupoSprites):
                sprite.physics.fixScreenPosition((self.scrollx, 0))

            # Ademas, actualizamos el decorado para que se muestre una parte distinta
            self.decorado.update(self.scrollx)

    def update(self, tiempo):
        self.time = tiempo
        self.grupoSpritesDinamicos.update(self)
        self.collisionUpdate()
        self.actualizarScroll(self.drin)
        self.fondo.update(tiempo)
        self.respawn.updateEnemies()
        self.textoVida.updateText(str(int(self.drin.getActualHP())))

        enmiesRemainig = self.respawn.enemiesRemaining()
        self.textoEnemiesRemaining.updateText('Enemigo restantes   ' + str(enmiesRemainig))
        if (enmiesRemainig <= 0):
            if (self.nextPhase == None):
                self.gameSuccedded()
            else:
                self.drin.completlyHeal()
                self.director.setDr1n(self.drin)
                self.phaseSuccedded()


    def collisionUpdate(self):
        self.collision(self.grupoEnemigos, self.grupoJugadores,  False, False, self.behHurts)
        self.collision(self.grupoDisparosEnemigo,self.grupoJugadores, True, False, self.behHurts)
        self.collision(self.grupoGolpesEnemigo,self.grupoJugadores , False, False, self.behHurts)
        self.collision(self.grupoDisparosJugador, self.grupoEnemigos, True, False, self.behHurts)
        self.collision(self.grupoDisparosJugador, self.grupoDisparosEnemigo, True, True)
        self.collision(self.grupoGolpesJugador, self.grupoEnemigos, False, False, self.behHurts)

        #Las trampas hacen daño
        self.collision(self.grupoTraps, self.grupoEnemigos,  False, False, self.behHurts)
        self.collision(self.grupoTraps, self.grupoJugadores,  False, False, self.behHurts)

        #El vacio mata
        self.collision(self.grupoVoid, self.grupoEnemigos,  False, False, self.behHurts)
        self.collision(self.grupoJugadores, self.grupoVoid,  True, False, self.behGameOver)


    def collision(self,group1, group2, destroy1, destroy2, behaviour=None):
        collision = pygame.sprite.groupcollide(group1, group2, destroy1, destroy2)
        if collision != {} and behaviour !=None:
            behaviour(collision)

    def behGameOver(self, collision):
        self.gameOver()

    def phaseSuccedded(self):
        self.drin.completlyHeal()
        self.director.setDr1n(self.drin)
        self.director.cambiarEscena(Interfase(self.director, self.nextPhase))

    def gameSuccedded(self):
        self.drin.completlyHeal()
        self.director.setDr1n(self.drin)
        self.director.cambiarEscena(EndOfGame(self.director, True))

    def gameOver(self):
        self.drin.completlyHeal()
        self.director.setDr1n(self.drin)
        self.director.cambiarEscena(EndOfGame(self.director, False))

    def behHurts(self, collision):
        for sprite in collision:
            damagedUnit = collision[sprite][0]
            if not damagedUnit.stats.getGhostMode():
                damagedUnit.hurt(sprite.stats.getDamage())
                damagedUnit.physics.incrementPosition((sprite.graphics.direction*100,0))

    def hdModeActivated(self):
    	return self.hdMode
        
    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.fondo.dibujar(pantalla)
        # Después el decorado
        self.decorado.dibujar(pantalla)
        # Luego los Sprites

        self.grupoPlatformsFill.draw(pantalla)
        self.grupoPlatforms.draw(pantalla)
        self.grupoTraps.draw(pantalla)
        self.grupoFloorFill.draw(pantalla)
        self.grupoFloor.draw(pantalla)
        self.grupoEnemigos.draw(pantalla)
        self.grupoJugadores.draw(pantalla)
        self.grupoDisparosJugador.draw(pantalla)
        self.grupoDisparosEnemigo.draw(pantalla)

        self.textoEnemiesRemaining.dibujar(pantalla)
        self.textoVida.dibujar(pantalla)
        self.botonVida.dibujar(pantalla)

        #self.grupoSprites.draw(pantalla)


    def collideWithPlatform(self, actor): 
        for plat in pygame.sprite.spritecollide(actor, self.grupoPlatforms, False):
            if (actor.rect.bottom < plat.rect.top or actor.rect.bottom < plat.rect.bottom):
                return True
        return False

    def collideWithFloor(self, actor): 
        for plat in pygame.sprite.spritecollide(actor, self.grupoFloor, False):
            if actor.rect.bottom < plat.rect.top or actor.rect.bottom < plat.rect.bottom:
                return True
        return False

    def collideWithVoid(self, actor): 
        for plat in pygame.sprite.spritecollide(actor, self.grupoVoid, False):
            if actor.rect.bottom < plat.rect.top or actor.rect.bottom < plat.rect.bottom:
                return True
        return False

    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()
        if (pygame.key.get_pressed()[K_p]):
        	self.hdMode = not self.hdMode
        # DRIN recieves all keys pressed this frame
        self.drin.setKeys(pygame.key.get_pressed())


# -------------------------------------------------
# Clases GUI

class TextoVida(TextoGUI):
    def __init__(self, pantalla, vida):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font("src/resources/fonts/gameFont.ttf", 42)
        TextoGUI.__init__(self, pantalla, fuente, (186, 0, 124), str(vida), (70, 70))

class TextoEnemiesRemaining(TextoGUI):
    def __init__(self, pantalla, enemigos):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font("src/resources/fonts/gameFont.ttf", 42)
        TextoGUI.__init__(self, pantalla, fuente, (186, 0, 124), 'Enemigo restantes   ' + str(enemigos), (ANCHO_PANTALLA - 395, 70))


class BotonVida(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'icons\life.png', (20, 70))

# -------------------------------------------------
# Clase Cielo

class Cielo:
    def __init__(self, image):
        imgFile = GestorRecursos.GetImageFileName(image) 
        self.sol = GestorRecursos.CargarImagen(imgFile, -1)
        self.sol = pygame.transform.scale(self.sol, (300, 200))

        self.rect = self.sol.get_rect()
        self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
        self.update(0)

    def update(self, tiempo):
        self.posicionx += VELOCIDAD_SOL * tiempo
        if (self.posicionx - self.rect.width >= ANCHO_PANTALLA):
            self.posicionx = 0
        self.rect.right = self.posicionx
        # Calculamos el color del cielo
        if self.posicionx >= ((self.rect.width + ANCHO_PANTALLA) / 2):
            ratio = 2 * ((self.rect.width + ANCHO_PANTALLA) - self.posicionx) / (self.rect.width + ANCHO_PANTALLA)
        else:
            ratio = 2 * self.posicionx / (self.rect.width + ANCHO_PANTALLA)
        self.colorCielo = (100*ratio, 200*ratio, 255)
        
    def dibujar(self,pantalla):
        # Dibujamos el color del cielo
        pantalla.fill(self.colorCielo)
        # Y ponemos el sol
        #pantalla.blit(self.sol, self.rect)

# -------------------------------------------------
# Clase Decorado

class Decorado:
    def __init__(self, image, large):

        imgFile = GestorRecursos.GetImageFileName(image)     
        self.imagen = GestorRecursos.CargarImagen(imgFile, -1)
        self.imagen = pygame.transform.scale(self.imagen, (large, 300))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)

