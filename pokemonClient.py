#!/usr/bin/env python3

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from PIL import Image
import io
import numpy as np
import getpass
import tkinter
import socket
import sys

CODIGO_YES = bytearray([30])
CODIGO_NO = bytearray([31])
CODIGO_LOGOUT = bytearray([32])
CODIGO_ACK = bytearray([33])

def login(soc):
    """Transfiere los datos al servidor para validar el acceso, y cierra el programa si los datos no son válidos
    
    :param soc: Socket de la conexión
    :type soc: Socket
    :returns: Nada
    """
    print("Ingrese el nombre de usuario con el que está registrado")
    user = input(" >> ")
    
    print("Ingrese la contraseña")
    psswd = getpass.getpass(" >> ")
    
    soc.send(user.encode(encoding='UTF-8'))
    soc.recv(1)
    soc.send(psswd.encode(encoding='UTF-8'))
    
    access = soc.recv(1)
    access = int.from_bytes(access,"big")
    if access == 0:
        print("Datos incorrectos")
        sys.exit()

def playPokemon(soc):
    """Permite que el usuario juegue Pokemon Go

    :param soc: Socket de la conexión
    :type soc: Socket
    :returns: Nada
    """
    try:
        soc.send(bytearray([10]))
        mensaje = soc.recv(2)
        #print(mensaje[0])
        idPokemon = mensaje[1]
        print("¿Capturar al Pokemon " + str(idPokemon) + "?")
        print("Sí [S] o No [N]")
        message = input(" >> ")
        
        if message == 'S':    
            soc.send(CODIGO_YES) 
            jugando = True
            while jugando:
                mensaje = soc.recv(10)
                respuesta = mensaje[0]
                
                if respuesta == 21: #aun tienes intentos
                    print("¿Intentar captura de nuevo? Quedan " + str(mensaje[2]) + " intentos")
                    print("Sí [S] o No [N]")
                    message = input(" >> ")
                    mensaje_correcto = False
                    while mensaje_correcto == False:
                        if message == 'S' or message == 'N':
                            mensaje_correcto = True
                        else:
                            print("Opción inválida >:(")
                            print("¿Intentar captura de nuevo? Quedan " + str(mensaje[2]) + " intentos")
                            print("Sí [S] o No [N]")
                            message = input(" >> ")
                    if message == 'S':
                        soc.send(CODIGO_YES)
                    else:
                        jugando = False
                else:
                    if respuesta == 22:#capturaste al pokemon
                        print("Capturaste al pokemon...")
                        soc.send(CODIGO_ACK)
                        img_size = int.from_bytes(soc.recv(4),"big")
                        soc.send(CODIGO_ACK)
                        img_bytes = soc.recv(img_size)
                        muestraPokemon(img_bytes)
                        jugando = False
                    if respuesta == 23:#te quedaste sin intentos
                        print("Te quedaste sin intentos :(")
                        jugando = False
            cerrarSesion(soc)
        else:
            cerrarSesion(soc)
    except socket.timeout :
        print("Tiempo de respuesta excedido: 10 segundos")
        cerrarSesion(soc)
        sys.exit()
    except IndexError:
        terminarConexion()

def muestraPokemon(bytes):
    """Despliega el pokemon asignado
    
    :param bytes: bytes de la imagen del pokemon a desplegar
    :type soc: bytearray
    :returns: Nada
    """
    image = Image.open(io.BytesIO(bytes))
    data = np.array(image)
    plt.imshow(data)
    plt.axis('off')
    plt.show()

def muestraPokedex(soc, usuario):
    try:
        print("Mostrando Pokedex...")
        soc.send(bytearray([11]))
        respuesta = soc.recv(1)[0]
        if respuesta == 24:
            soc.send(CODIGO_ACK)
            size_pokedex = int.from_bytes(soc.recv(4),"big")
            soc.send(CODIGO_ACK)
            pokedex = []
            for i in range(size_pokedex):
                pokemon_size = int.from_bytes(soc.recv(1),"big")
                soc.send(CODIGO_ACK)
                modelo = soc.recv(pokemon_size)
                pokemon = modelo.decode("utf-8")
                pokedex.append(pokemon)
            displayPokedex(pokedex)
    except socket.timeout:
        print("Tiempo de respuesta excedido: 10 segundos")
        cerrarSesion(soc)
        sys.exit()
    except IndexError :
        terminarConexion()

def displayPokedex(pokedex):
    for col1,col2 in zip(pokedex[::2],pokedex[1::2]):
	    print(col1+",",col2+",")

def muestraCatalogo(soc, usuario):
    try:
        print("Mostrando catálogo...")
        soc.send(bytearray([12]))
        respuesta = soc.recv(1)[0]
        if respuesta == 25:
            soc.send(CODIGO_ACK)
            size_catalogo = int.from_bytes(soc.recv(4),"big")
            soc.send(CODIGO_ACK)
            catalogo = []
            for i in range(size_catalogo):
                pokemon_size = int.from_bytes(soc.recv(1),"big")
                soc.send(CODIGO_ACK)
                modelo = soc.recv(pokemon_size)
                pokemon = modelo.decode("utf-8")
                catalogo.append(pokemon)
            displayCatalogo(catalogo)
    except socket.timeout:
        print("Tiempo de respuesta excedido: 10 segundos")
        cerrarSesion(soc)
        sys.exit()
    except IndexError :
        terminarConexion()

def displayCatalogo(catalogo):
    for col1,col2,col3,col4,col5,col6 in zip(catalogo[::6],catalogo[1::6],catalogo[2::6],catalogo[3::6],catalogo[4::6],catalogo[5::6]):
        print (col1+",",col2+",",col3+",",col4+",",col5+",",col6+",")

def cerrarSesion(soc):
    """Cierre normal de sesión del usuario
    
    :param soc: Socket de la conexión
    :type soc: Socket
    :returns: Nada
    """
    print("Terminando conexión...")
    soc.send(CODIGO_LOGOUT)

def terminarConexion():
    """Revisa el status del socket. Si esta cerrada la conexion
       entonces cierra la sesión por tiempo de espera excedido
    
    :param soc: Socket de la conexión
    :type soc: Socket
    :returns: Nada
    """
    print("Tiempo de respuesta excedido: 10 segundos")
    print("Terminando conexión...")
    sys.exit(1)


def main():
    """ Función principal
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = sys.argv[1]
    port = int(sys.argv[2])
    try:
        soc.connect((host, port))
        #soc.settimeout(10)
    except:
        print("Connection Error")
        sys.exit()
    login(soc)
    opcion_correcta = False
    try:
        while opcion_correcta == False:
            print("Bienvenido a Pokemon Go! ¿Deseas capturar un Pokémon [P], revisar el Pokedex [X], revisar el catálogo? [C] o salir [S]?")
            message = input(" >> ")
            if message == 'S' or message == 'P' or message == 'C' or message == 'X' :
                opcion_correcta = True
    except socket.timeout:
        print("Tiempo de respuesta excedido: 10 segundos")
        cerrarSesion(soc)
        sys.exit()
    except IndexError :
        terminarConexion()
    if message != 'S':
            if message == 'P':
                playPokemon(soc)
            if message == 'X':
                muestraPokedex(soc, "usuario")
            if message == 'C':
                muestraCatalogo(soc,"usuario")

    else:
            cerrarSesion(soc)
        
if __name__ == "__main__":
   main()
