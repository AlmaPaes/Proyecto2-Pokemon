#!/usr/bin/env python3

import socket
import sys
import traceback
import threading 
import random

def main():
    """ Función principal.
    """
    start_server()
   
def start_server():
    """Inicialización del servidor

    :returns: Nada
    """
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
    """Manejador del hilo que sostiene la conexión entre el servidor y un cliente
    
    :param connection: Conexión entre el servidor y el cliente que abrió el hilo
    :type connection: Conexión
    :param ip: Dirección IP de la conexión
    :type ip: Cadena
    :param port: Puerto a través del cual el servidor mantiene la conexión con el cliente
    :type port: Entero
    :param max_buffer_size: Número máximo de bytes que puede recibir en un paquete del cliente
    :type max_buffer_size: Entero
    :returns: Nada
    """
    connection.settimeout(10)     #Establecemos timeout a cada hilo
    is_active = True
    if giveAccess(connection) == 0:
        is_active = False
    
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
            cerrarSesion(connection)
            is_active = False       
    cerrarSesion(connection)
    
def giveAccess(connection,max_buffer_size = 5120):
    """Autentifica a usuarios registrados y proporciona acceso a la ejecución de la aplicación
    
    :param connection: Conexión entre el servidor y el cliente que abrió el hilo
    :type connection: Conexión
    :param max_buffer_size: Número máximo de bytes que puede recibir en un paquete del cliente
    :type max_buffer_size: Entero
    :returns: int - Indicador de acceso permitido
    """
    user = connection.recv(max_buffer_size)
    user = user.decode('UTF-8')

    connection.send(bytearray([0]))
    
    psswd = connection.recv(max_buffer_size)
    psswd = psswd.decode('UTF-8')
    
    s1 = 'Alma'
    s2 = 'alma'
    acceso = 0
    
    if s1 == user and s2 == psswd:
        acceso = 1
        
    #resp = int.from_bytes(connection.recv(1),"big")
    connection.send(bytearray([acceso]))
    
    return acceso
          
def playPokemonGo(connection):
    """
    Método que simula el comportamiento del juego Pokemon Go
    
    :param connection: Conexión entre el servidor y el cliente
    :type connection: Conexión
    :returns: Nada
    """
    try:
        setIdPokemon = random.randint(0,151)
        setPokemon = [20,setIdPokemon]
        connection.send(bytearray(setPokemon))
        intentos = random.randint(1,5)
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
                            fallido = [21,setIdPokemon,intentos_disponibles]
                            intento_actual = intento_actual + 1
                            connection.send(bytearray(fallido))
                        else: #capturado
                            connection.send(bytearray([22]))
                            jugando = False
                else:#ya no quiere jugar
                    jugando = False
            except socket.timeout as timeout:
                print("Tiempo de respuesta excedido: 10 segundos")
                #sys.exit()
                #connection.send(bytearray([40])) -> Mensaje de error
                cerrarSesion(connection)
                jugando = False
        
        #print("bai")
    except socket.timeout as timeout:
        print("Tiempo de respuesta excedido: 10 segundos")
        #sys.exit()
        cerrarSesion(connection)
    
def cerrarSesion(connection):
    """Cierre de sesión entre el servidor y el cliente al cual le pertenece la conexión
    
    :param connection: Conexión entre el cliente y el servidor
    :returns: Nada
    """
    #connection.shutdown(socket.SHUT_RDWR)
    connection.close()
    
if __name__ == "__main__":
   main()
