#!/usr/bin/env python3

import socket
import sys

CODIGO_YES = bytearray([30])
CODIGO_NO = bytearray([31])


def main():
   soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   host = "127.0.0.1"
   port = 9999
   try:
      soc.connect((host, port))
   except:
      print("Connection Error")
      sys.exit()
   print("Bienvenido a Pokemon Go! ¿Deseas capturar un Pokémon [P], revisar el catálogo? [C] o salir [S]?")
   message = input(" >> ")
   if message != 'S':
        if message == 'P':
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
                    mensaje = soc.recv(10)
                    #print(mensaje[0])
                    respuesta = mensaje[0]
                    
                    #respuesta = int.from_bytes(mensaje[0],"big")
                    
                    if respuesta == 21: #aun tienes intentos
                        print("¿Intentar captura de nuevo? Quedan " + str(mensaje[2]) + " intentos")
                        message = input(" >> ")
                        soc.send(CODIGO_YES)
                    else:
                        if respuesta == 22:#capturaste al pokemon
                            print("Capturaste al pokemon")
                            jugando = False
                        if respuesta == 23:#te quedaste sin intentos
                            print("Te quedaste sin intentos :(")
                            jugando = False
                        #if message == 'S':
                        #    soc.send(CODIGO_YES)
            #else:
                print("terminando sesión")
                        
            print("bai")
            #print("hola")
        #else:
        #    soc.send(bytes([11]))
          
        #if soc.recv(5120).decode("utf8") == "-":
        #    pass # null operation
        
if __name__ == "__main__":
   main()
