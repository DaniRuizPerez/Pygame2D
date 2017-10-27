# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *

import xml.etree.ElementTree as ET

# -------------------------------------------------
# Clase GestorRecursos

# En este caso se implementa como una clase vacía, solo con métodos de clase
folder = "src\\resources\imagenes"
faseFolder = "src\game_logic"
imageNamesFile = "src\\resources\\routesById.xml"
class GestorRecursos(object):
    recursos = {}
    imagesNames = {}
    tree = ET.parse(imageNamesFile)
            
    @classmethod
    def CargarImagen(cls, nombre, colorkey=None):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join(folder, nombre)
            try:
                imagen = pygame.image.load(fullname)
            except pygame.error, message:
                print 'Cannot load image:', fullname
                raise SystemExit, message
            imagen = imagen.convert()
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = imagen.get_at((0,0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.recursos[nombre] = imagen
            # Se devuelve
            return imagen

    @classmethod
    def CargarArchivoCoordenadas(cls, nombre):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join(folder, nombre)
            pfile=open(fullname,'r')
            datos=pfile.read()
            pfile.close()
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos


    @classmethod
    def GetImageFileName(cls, nombre):

        if nombre in cls.imagesNames:
            # Se devuelve ese recurso
            return cls.imagesNames[nombre]
        
        root = cls.tree.getroot()
        if root.tag != 'routes' :
            raise Exception('Route Names parser error: ' + nombre + ' not file found')

        for image in root.findall( 'route' ):
            if image.find( 'name' ).text == nombre:
                cls.imagesNames[nombre] = image.find( 'file' ).text
                return image.find( 'file' ).text

        raise Exception('Images Names parser error: ' + nombre + ' name not found in file')


    @classmethod
    def CargarFase(cls, nombre):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join(faseFolder, nombre + '.xml')
            try:
                tree = ET.parse(fullname)
                root = tree.getroot()

                if root.tag != 'stage' :
                    raise Exception('Stage parser error: ' + nombre + ' not stage tag found')

            except pygame.error, message:
                print 'Cannot load fase:', fullname
                raise SystemExit, message
            # Se almacena
            cls.recursos[nombre] = root
            # Se devuelve
            return root