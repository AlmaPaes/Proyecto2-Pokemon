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

def printCharizard():
    print("                 .\"-,.__\n")
    print("                 `.     `.  ,\n")
    print("              .--'  .._,'\"-' `.\n")
    print("             .    .'         `'\n")
    print("             `.   /          ,'\n")
    print("               `  '--.   ,-\"'\n")
    print("                `\"`   |  \\\n")
    print("                   -. \\, |\n")
    print("                    `--Y.'      ___.\n")
    print("                         \\     L._, \\\n")
    print("               _.,        `.   <  <\\                _\n")
    print("             ,' '           `, `.   | \\            ( `\n")
    print("          ../, `.            `  |    .\\`.           \\ \\_\n")
    print("         ,' ,..  .           _.,'    ||\\l            )  '\".\n")
    print("        , ,'   \\           ,'.-.`-._,'  |           .  _._`.\n")
    print("      ,' /      \\ \\        `' ' `--/   | \\          / /   ..\\\n")
    print("    .'  /        \\ .         |\\__ - _ ,'` `        / /     `.`.\n")
    print("    |  '          ..         `-...-\"  |  `-'      / /        . `.\n")
    print("    | /           |L__           |    |          / /          `. `.\n")
    print("   , /            .   .          |    |         / /             ` `\n")
    print("  / /          ,. ,`._ `-_       |    |  _   ,-' /               ` \\\n")
    print(" / .           \\\"`_/. `-_ \\_,.  ,'    +-' `-'  _,        ..,-.    \\`.\n")
    print(".  '         .-f    ,'   `    '.       \\__.---'     _   .'   '     \\ \\\n")
    print("' /          `.'    l     .' /          \\..      ,_|/   `.  ,'`     L`\n")
    print("|'      _.-\"\"` `.    \\ _,'  `            \\ `.___`.'\"`-.  , |   |    | \\\n")
    print("||    ,'      `. `.   '       _,...._        `  |    `/ '  |   '     .|\n")
    print("||  ,'          `. .,.---' ,'       `.   `.. `-'  .-' /_ .'    _   ||\n")
    print("|| '              V      / /           `   | `   ,'   ,' '.    !  `. ||\n")
    print("||/            _,-------7 '              . |  `-'    l         /    `||\n")
    print(". |          ,' .-   ,' ||               | .-.        `.      .'     ||\n")
    print(" `'        ,'    `\".'    |               |    `.        '. -.'       `'\n")
    print("          /      ,'      |               |,'    \\-.._,.'/'\n")
    print("          .     /        .               .       \\    .''\n")
    print("        .`.    |         `.             /         :_,'.'\n")
    print("          \\ `...\\   _     ,'-.        .'         /_.-'\n")
    print("           `-.__ `,  `'   .  _.>----''.  _  __  /\n")
    print("                .'        /\"'          |  \"'   '_\n")
    print("               /_|.-'\\ ,\".             '.'`__'-( \\\n")
    print("                 / ,\"'\"\\,'               `/  `-.|\" mh\n")

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
    if access == 51:
        print("Datos incorrectos")
        sys.exit()

def playPokemon(soc):
    """Permite que el usuario juegue Pokemon Go.

    :param soc: Socket de la conexión
    :type soc: Socket
    :returns: Nada
    """
    try:
        soc.send(bytearray([10]))
        mensaje = soc.recv(2)
        idPokemon = mensaje[1]
        nombrePokemon = soc.recv(50).decode("utf-8")
        print("¿Capturar al Pokemon " + nombrePokemon + "?")
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
    except socket.timeout : #No recibe respuesta del servidor
        terminarConTimeout(soc)
    except IndexError: #El Servidor manda un timeout
        terminarConexion()

def muestraPokemon(bytes):
    """Despliega el pokemon asignado.
    
    :param bytes: bytes de la imagen del pokemon a desplegar
    :type bytes: bytearray
    :returns: Nada
    """
    image = Image.open(io.BytesIO(bytes))
    data = np.array(image)
    plt.imshow(data)
    plt.axis('off')
    plt.show()

def muestraPokedex(soc):
    """Muestra el Pokedex del usuario que solicita esta acción
       al usuario.
    
    :param soc: Socket de la conexión
    :type soc: Socket
    :returns: Nada
    """
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
    except socket.timeout: #No recibe respuesta del servidor
        terminarConTimeout(soc)
    except IndexError : #El Servidor manda un timeout
        terminarConexion()

def displayPokedex(pokedex):
    """Imprime en pantalla el Pokedex de manera
       "amigable".
    
    :param pokedex: Pokedex de Pokemones 
    :type pokedex: List of String
    :returns: Nada
    """
    for col1,col2 in zip(pokedex[::2],pokedex[1::2]):
	    print(col1+",",col2+",")

def muestraCatalogo(soc):
    """Le muestra el catalogo disponible de Pokemones
       al usuario.
    
    :param soc: Socket de la  conexión
    :type soc: Socket
    :returns: Nada
    """
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
    except socket.timeout: #No recibe respuesta del servidor
        terminarConTimeout(soc)
    except IndexError : #El Servidor manda un timeout
        terminarConexion()

def displayCatalogo(catalogo):
    """Imprime en pantalla el catalogo de Pokemones
       disponibles de manera "amigable".
    
    :param catalogo: Catalogo de Pokemones 
    :type catalogo: List of String
    :returns: Nada
    """
    for col1,col2,col3,col4,col5,col6 in zip(catalogo[::6],catalogo[1::6],catalogo[2::6],catalogo[3::6],catalogo[4::6],catalogo[5::6]):
        print (col1+",",col2+",",col3+",",col4+",",col5+",",col6+",")

def cerrarSesion(soc):
    """Cierre normal de sesión del usuario.
    
    :param soc: Socket de la conexión
    :type soc: Socket
    :returns: Nada
    """
    print("Terminando conexión...")
    soc.send(CODIGO_LOGOUT)

def terminarConexion():
    """Termina la conexion pues el Servidor notifica que
       el tiempo de espera ha excedido.
    
    :param soc: Nada
    :returns: Nada
    """
    print("Tiempo de respuesta excedido: 10 segundos")
    print("Terminando conexión...")
    sys.exit(1)

def terminarConTimeout(soc):
    """Termina la conexion pues el tiempo de espera de la 
        respuesta del Servidor ha excedido.
        
    :param soc: Socket de la conexión
    :type soc: Socket
    :returns: Nada
    """

    print("Falló la conexión con el servidor...")
    print("Terminando conexión...")
    soc.close()
    sys.exit(1)

def main():
    """ Función principal
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = sys.argv[1]
    port = int(sys.argv[2])
    try:
        soc.connect((host, port))
        soc.settimeout(20)
    except:
        print("Connection Error")
        sys.exit()
    login(soc)
    #printCharizard()
    opcion_correcta = False
    try:
        while opcion_correcta == False:
            print("Bienvenido a Pokemon Go! ¿Deseas capturar un Pokémon [P], revisar el Pokedex [X], revisar el catálogo? [C] o salir [S]?")
            message = input(" >> ")
            if message == 'S' or message == 'P' or message == 'C' or message == 'X' :
                opcion_correcta = True
    except socket.timeout: #No recibe respuesta del servidor
        terminarConTimeout(soc)
    except IndexError : #El Servidor manda un timeout
        terminarConexion()
    if message != 'S':
            if message == 'P':
                playPokemon(soc)
            if message == 'X':
                muestraPokedex(soc)
            if message == 'C':
                muestraCatalogo(soc)

    else:
            cerrarSesion(soc)
        
if __name__ == "__main__":
   main()
