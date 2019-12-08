#!/usr/bin/env python3

import socket
import sys
import traceback
import threading 
import random

def main():
   start_server()
   
def start_server():
   host = "127.0.0.1"
   port = 9999 # arbitrary non-privileged port
   soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   print("Socket created")
   try:
      soc.bind((host, port))
   except:
      print("Bind failed. Error : " + str(sys.exc_info()))
      sys.exit()
   soc.listen(6) # queue up to 6 requests
   print("Socket now listening")
   # infinite loop => do not reset for every requests
   while True:
        #connection = host | address = port
        connection, address = soc.accept() 
        #soc.settimeout(10)  
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        try:
            threading.Thread(target=clientThread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()
   soc.close()

def clientThread(connection, ip, port, max_buffer_size = 5120):
   connection.settimeout(10)     #Establecemos timeout a cada hilo
   is_active = True
   while is_active:
      #client_input = receive_input(connection, max_buffer_size) 
      try:
        client_input = connection.recv(max_buffer_size)
        codigo = int.from_bytes(client_input,"big")
        if codigo == 10:
            playPokemonGo(connection)
            is_active = False
        if codigo == 32:
            is_active = False
            #print(connection.fileno()) -> socket.status
      except socket.timeout as timeout:
          print("Tiempo de respuesta excedido: 10 segundos")
          avisoTimeout(connection)
          cerrarSesion(connection)
          is_active = False       
   cerrarSesion(connection)
          
def playPokemonGo(connection):
    try:
        setIdPokemon = random.randint(1,151)
        setPokemon = [20,setIdPokemon]
        connection.send(bytearray(setPokemon))
        intentos = random.randint(1,6)
        print("Jugando!")
        print("Número de intentos: " + str(intentos))
        intento_acertado = random.randint(1,intentos)
        intentos_disponibles = intentos
        intento_actual = 1
        jugando = True

        while jugando:
            try:
                respuesta = connection.recv(1)
                respuesta = int.from_bytes(respuesta,"big")
                if respuesta == 30:
                    if intentos_disponibles == 0: #ya no hay intentos disponibles
                        connection.send(bytearray([23]))
                        jugando = False
                    else:
                        if intento_actual != intento_acertado: #no ha capturado el pokemon
                            intentos_disponibles = intentos_disponibles - 1
                            fallido = bytearray([21,setIdPokemon,intentos_disponibles])
                            intento_actual = intento_actual + 1
                            connection.send(fallido)
                        else: #capturado
                            msg = bytearray([22,setIdPokemon])
                            connection.send(msg)
                            ruta_img = "pokemons/"
                            ruta_img += str(setIdPokemon) + ".png"
                            img = open(ruta_img, 'rb')
                            bytes = img.read()
                            size = len(bytes)
                            size_bytes = size.to_bytes(4, 'big')
                            if connection.recv(1)[0] == 33:
                                connection.send(size_bytes)
                            if connection.recv(1)[0] == 33:
                                connection.send(bytes)
                            jugando = False
                else:#ya no quiere jugar
                    jugando = False
            except socket.timeout as timeout:
                print("Tiempo de respuesta excedido: 10 segundos")
                avisoTimeout(connection)
                cerrarSesion(connection)
                jugando = False
        
        #print("bai")
    except socket.timeout as timeout:
        print("Tiempo de respuesta excedido: 10 segundos")
        avisoTimeout(connection)
        cerrarSesion(connection)
    
def cerrarSesion(connection):
    connection.close()

def avisoTimeout(connection):
    connection.send(bytearray([40]))
    
'''         
def receive_input(connection, max_buffer_size):
   client_input = connection.recv(max_buffer_size)
   client_input_size = sys.getsizeof(client_input)
   if client_input_size > max_buffer_size:
      print("The input size is greater than expected {}".format(client_input_size))
   decoded_input = client_input.decode("utf8").rstrip()
   result = process_input(decoded_input)
   return result
def process_input(input_str):
   print("Processing the input received from client")
   return "Hello " + str(input_str).upper()
'''
if __name__ == "__main__":
   main()
