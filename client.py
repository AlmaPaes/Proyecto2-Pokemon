#!/usr/bin/env python3

import socket
import sys

CODIGO_YES = bytearray([30])
CODIGO_NO = bytearray([31])
CODIGO_LOGOUT = bytearray([32])

def login(soc):
    """Transfiere los datos al servidor para validar el acceso, y cierra el programa si los datos no son válidos
    
    :param soc: Socket de la conexión
    :type soc: Socket
    :returns: Nada
    """
    print("Ingrese el nombre de usuario con el que está registrado")
    user = input(" >> ")
    
    print("Ingrese la contraseña")
    psswd = input(" >> ")
    
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
        idPokemon = mensaje[1]
        print("¿Capturar al Pokemon " + str(idPokemon) + "?")
        print("Sí [S] o No [N]")
        message = input(" >> ")
        
        if message == 'S':
            soc.send(CODIGO_YES) 
            jugando = True
            while jugando:
                try:
                    mensaje = soc.recv(10)
                    #print(mensaje[0])
                    respuesta = mensaje[0]
                    
                    #respuesta = int.from_bytes(mensaje[0],"big")
                    
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
                            #cerrarSesion(soc)
                    else:
                        if respuesta == 22:#capturaste al pokemon
                            print("Capturaste al pokemon")
                            jugando = False
                        if respuesta == 23:#te quedaste sin intentos
                            print("Te quedaste sin intentos :(")
                            jugando = False
                        #cerrarSesion(soc)
                        #if message == 'S':
                        #    soc.send(CODIGO_YES)
                except socket.timeout as timeout:
                    print("Tiempo de respuesta excedido: 10 segundos")
                    #sys.exit()
                    cerrarSesion(soc)
            cerrarSesion(soc)
        else:
            #print("Gracias por jugar, hasta la próxima!")
            cerrarSesion(soc)
            #print(soc.fileno()) -> status.socket
    except socket.timeout as timeout:
        print("Tiempo de respuesta excedido: 10 segundos")
        #sys.exit()
        cerrarSesion(soc)
    #else:
        

def cerrarSesion(soc):
    """Cierre de sesión del usuario
    
    :param soc: Socket de la conexión
    :type soc: Socket
    :returns: Nada
    """
    print("Terminando conexión...")
    soc.send(CODIGO_LOGOUT)
    
    
def main():
    """ Función principal
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = sys.argv[1]
    port = sys.argv[2]
    try:
        soc.connect((host, port))
        soc.settimeout(10)
    except:
        print("Connection Error")
        sys.exit()
    login(soc)
    opcion_correcta = False
    while opcion_correcta == False:
        print("Bienvenido a Pokemon Go! ¿Deseas capturar un Pokémon [P], revisar el catálogo? [C] o salir [S]?")
        message = input(" >> ")
        if message == 'S' or message == 'P' or message == 'C':
            opcion_correcta = True

    if message != 'S':
            if message == 'P':
                playPokemon(soc)
            else:
                print("Mostrando catálogo")

    else:
            cerrarSesion(soc)
        
if __name__ == "__main__":
   main()
