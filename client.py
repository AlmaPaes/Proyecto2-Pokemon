#!/usr/bin/env python3
import socket
import sys

CODIGO_YES = bytearray([30])
CODIGO_NO = bytearray([31])
CODIGO_LOGOUT = bytearray([32])

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
                            cerrarSesion(soc)
                    else:
                        if respuesta == 22:#capturaste al pokemon
                            print("Capturaste al pokemon")
                            jugando = False
                        if respuesta == 23:#te quedaste sin intentos
                            print("Te quedaste sin intentos :(")
                            jugando = False
                        #if message == 'S':
                        #    soc.send(CODIGO_YES)
                    cerrarSesion(soc)
                except socket.timeout as timeout:
                    print("Tiempo de respuesta excedido: 10 segundos")
                    sys.exit()
    except socket.timeout as timeout:
        print("Tiempo de respuesta excedido: 10 segundos")
        sys.exit()
    #else:
        

def cerrarSesion(soc):
    print("Terminando conexión")
    soc.send(CODIGO_LOGOUT)
    
def main():
   soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   host = "127.0.0.1"
   port = 9999
   try:
      soc.connect((host, port))
      soc.settimeout(10)
   except:
      print("Connection Error")
      sys.exit()
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
            #print("hola")
            soc.send(bytearray([10]))
            msg_recived = soc.recv(2)
            print("Codigo: %i | idPokemon: %i"%(msg_recived[0], msg_recived[1]))
        #else:
        #    soc.send(bytes([11]))
          
        #if soc.recv(5120).decode("utf8") == "-":
        #    pass # null operation
        
if __name__ == "__main__":
   main()
