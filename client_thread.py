#!/usr/bin/env python3

import socket
import sys


def main():
   soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   host = "127.0.0.1"
   port = 9999
   try:
      soc.connect((host, port))
   except:
      print("Connection Error")
      sys.exit()
   print("Bienvenido a Pokemon Go! ¿Deseas capturar un Pokémon [P], revisar el catálogo? [C] o salir [S]")
   message = input(" >> ")
   if message != 'S':
        if message == 'P':
            soc.send(bytearray([10]))
            idPokemon = soc.recv(2)
            print(idPokemon)
        #else:
        #    soc.send(bytes([11]))
          
        if soc.recv(5120).decode("utf8") == "-":
            pass # null operation
        
if __name__ == "__main__":
   main()
