#!/usr/bin/env python3

import socket
import sys
import matplotlib.pyplot as plt
from PIL import Image
import io
import numpy as np

CODIGO_YES = bytearray([30])
CODIGO_NO = bytearray([31])
CODIGO_LOGOUT = bytearray([32])
CODIGO_ACK = bytearray([33])

def playPokemon(soc):
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
                    else:
                        if respuesta == 22:#capturaste al pokemon
                            #print("va bien")
                            soc.send(CODIGO_ACK)
                            print("Capturaste al pokemon: "+ str(mensaje[1]))
                            img_size = int.from_bytes(soc.recv(4),"big")
                            soc.send(CODIGO_ACK)
                            img_bytes = soc.recv(img_size)
                            muestraPokemon(img_bytes)
                            jugando = False
                        if respuesta == 23:#te quedaste sin intentos
                            print("Te quedaste sin intentos :(")
                            jugando = False
                        #if message == 'S':
                        #    soc.send(CODIGO_YES)
                except socket.timeout as timeout:
                    print("Tiempo de respuesta excedido: 10 segundos")
                    cerrarSesion(soc)
            cerrarSesion(soc)
        else:
            cerrarSesion(soc)
            #print(soc.fileno()) -> status.socket
    except socket.timeout as timeout:
        cerrarPorTimeout(soc)
        

def cerrarSesion(soc):
    print("Terminando conexión...")
    soc.send(CODIGO_LOGOUT)

def cerrarPorTimeout(soc):
    print("Tiempo de respuesta excedido: 10 segundos")
    cerrarSesion(soc)
    sys.exit()

def muestraPokemon(bytes):
    image = Image.open(io.BytesIO(bytes))
    data = np.array(image)
    plt.imshow(data)
    plt.axis('off')
    plt.show()
    
def main():
   soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   host = "127.0.0.1"
   port = 9999
   try:
      soc.connect((host, port))
      #soc.settimeout(10)
   except:
      print("Connection Error")
      sys.exit()
   opcion_correcta = False
   #try:
   while opcion_correcta == False:
       print("Bienvenido a Pokemon Go! ¿Deseas capturar un Pokémon [P], revisar el catálogo? [C] o salir [S]?")
       message = input(" >> ")
       if message == 'S' or message == 'P' or message == 'C':
           opcion_correcta = True
   #except socket.timeout as timeout:
    #   cerrarPorTimeout(soc)

   if message != 'S':
        if message == 'P':
            playPokemon(soc)
        else:
            print("Mostrando catálogo")

   else:
        cerrarSesion(soc)
            #print("hola")
        #else:
        #    soc.send(bytes([11]))
          
        #if soc.recv(5120).decode("utf8") == "-":
        #    pass # null operation
        
if __name__ == "__main__":
   main()
