#!/usr/bin/env python3

import mysql.connector as mysql
import socket
import sys
import traceback
import threading 
import random

#Configuracion para conectarse a la BD
CONFIG = {
    'user': 'doggos',
    'password': 'doggos2020',
    'host': 'localhost',
    'database': 'TCP201-Pokemon',
    'raise_on_warnings': True
}

IP = "127.0.0.1"
PORT = 9999

def main():
    """ Función principal.
    """
    start_server()
   
def start_server():
    """Inicialización del servidor
    
    :param ip_dir: Dirección IP del socket al cual se va aconectar el servidor
    :type ip_dir: Cadena
    :returns: Nada
    """
    host = IP
    port = PORT # arbitrary non-privileged port
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")
    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    soc.listen(10) # queue up to 10 requests
    print("Socket now listening")
    while True:
            #connection = host | address = port
            connection, address = soc.accept() 
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
    connection.settimeout(15)     #Establecemos timeout a cada hilo
    is_active = True
    acceso, user = giveAccess(connection)
    if acceso == 51:
        is_active = False
            
    while is_active: 
        try:
            client_input = connection.recv(max_buffer_size)
            codigo = int.from_bytes(client_input,"big")
            if codigo == 10:    #capturar pokemon
                playPokemonGo(connection, user)
                is_active = False
            if codigo == 11:    #ver pokedex
                muestraPokedex(connection, user)
                is_active = False
            if codigo == 12:    #ver catalogo
                muestraCatalogo(connection)
                is_active = False
            if codigo == 32:    #no quiere hacer algo
                is_active = False
        except socket.timeout :
            print("Tiempo de respuesta excedido: 10 segundos")
            avisoTimeout(connection)
            cerrarSesion(connection)
            is_active = False
        except IndexError:
            terminarConexion()

    cerrarSesion(connection)
   
def giveAccess(connection,max_buffer_size = 5120):
    """Autentifica a usuarios registrados y proporciona acceso a la ejecución de la aplicación
    
    :param connection: Conexión entre el servidor y el cliente que abrió el hilo
    :type connection: Conexión
    :param max_buffer_size: Número máximo de bytes que puede recibir en un paquete del cliente
    :type max_buffer_size: Entero
    :returns: Integer, String
    """
    ACCESO_PERMITIDO = 50
    ACCESO_DENEGADO = 51
    try:
        user = connection.recv(max_buffer_size)
        user = user.decode('UTF-8')

        connection.send(bytearray([0]))
    
        psswd = connection.recv(max_buffer_size)
        psswd = psswd.decode('UTF-8')
    except socket.timeout :
        print("Tiempo de respuesta excedido: 10 segundos")
        avisoTimeout(connection)
        cerrarSesion(connection)
    except IndexError:
        terminarConexion()
    
    cnx = mysql.connect(**CONFIG)
    cursor = cnx.cursor()
    
    correctPsswd = ""
    query = "SELECT Nombre,Pwd FROM Usuario WHERE Nombre = '" + user + "'"
    cursor.execute(query)
    todo = cursor.fetchone()
    if todo is not None:
        nombre = todo[0]
        correctPsswd = todo[1]
        
    acceso = ACCESO_DENEGADO
    if correctPsswd == psswd:
        acceso = ACCESO_PERMITIDO

    connection.send(bytearray([acceso]))
    
    return acceso, nombre
          
def playPokemonGo(connection, user):
    """
    Método que simula el comportamiento del juego Pokemon Go
    
    :param connection: Conexión entre el servidor y el cliente
    :type connection: Conexión
    :returns: Nada
    """
    try:
        setIdPokemon = random.randint(1,151)
        setPokemon = [20,setIdPokemon]
        connection.send(bytearray(setPokemon))
        nombrePokemon = getNombrePokemon(setIdPokemon)
        connection.send(nombrePokemon.encode("utf-8"))
        intentos = random.randint(1,5)
        print("Jugando!")
        print("Número de intentos: " + str(intentos))
        intento_acertado = random.randint(0,intentos)
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
                        cerrarSesion(connection)
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
                                guardaEnPokedex(setIdPokemon, user)
                            jugando = False
                else: #ya no quiere jugar
                    jugando = False
            except socket.timeout :
                print("Tiempo de respuesta excedido: 10 segundos")
                avisoTimeout(connection)
                cerrarSesion(connection)
                jugando = False
            except IndexError:
                terminarConexion()
    except socket.timeout as timeout:
        print("Tiempo de respuesta excedido: 10 segundos")
        avisoTimeout(connection)
        cerrarSesion(connection)
    except IndexError:
        terminarConexion()
    
def getNombrePokemon(idPokemon):
    """Regresa el nombre del pokemon dado su id
    
    :param idPokemon: Id del Pokemon a capturado
    :type idPokemon: Integer
    :returns: String
    """
    cnx = mysql.connect(**CONFIG)
    cursor = cnx.cursor()
    cursor.execute("SELECT Nombre FROM Pokemon WHERE idPokemon = %i"%(idPokemon))
    nombrePokemon = cursor.fetchone()[0]
    return nombrePokemon

def cerrarSesion(connection):
    """Cierre de sesión entre el servidor y el cliente al cual le pertenece la conexión
    
    :param connection: Conexión entre el cliente y el servidor
    :type connection: Conexión
    :returns: Nada
    """
    connection.close()

def terminarConexion():
    """Termina la conexion pues el Cliente notifica que
       el tiempo de espera ha excedido.
    
    :param: Nada
    :returns: Nada
    """
    print("Tiempo de respuesta excedido: 10 segundos")
    print("Terminando conexión...")
    sys.exit(1)

def avisoTimeout(connection):
    """Manda el mensaje de cierre de sesión al cliente por tiempo de espera excedido (timeout)
    
    :param connection: Conexión entre el cliente y el servidor
    :type connection: Conexión
    :returns: Nada
    """
    connection.send(bytearray([40]))

def guardaEnPokedex(idPokemon, user):
    """Guarda el pokemon capturado en el pokedex del
       usuario.
    
    :param idPokemon: Id del Pokemon a capturado
    :type idPokemon: Integer
    :param user: Usuario que capturo
    :type user: String
    :returns: Nada
    """
    cnx = mysql.connect(**CONFIG)
    cursor = cnx.cursor()
    userLogged = "'%s'" % user
    cursor.execute("SELECT idUsuario FROM Usuario WHERE Nombre = %s"%(userLogged))
    idUser = cursor.fetchone()[0]
    cursor.execute("INSERT INTO Pokedex (Usuario, Pokemon) VALUES (%i, %i)"%(idUser,idPokemon))
    cnx.commit()


def muestraPokedex(connection, user):
    """Muestra el Pokedex del usuario.
    
    :param connection: Conexión entre el servidor y el cliente
    :type connection: Conexión
    :param user: Usuario que capturo
    :type user: String
    :returns: Nada
    """
    try:
        cnx = mysql.connect(**CONFIG)
        cursor = cnx.cursor()
        userLogged = "'%s'" % user
        cursor.execute("SELECT idUsuario FROM Usuario WHERE Nombre = %s"%(userLogged))
        idUser = cursor.fetchone()[0]
        cursor.execute("SELECT Pokemon FROM Pokedex WHERE Usuario = %i"%(idUser))
        result = cursor.fetchall()
        pokedex = []
        for i in result:
            cursor.execute("SELECT Nombre FROM Pokemon WHERE idPokemon = %i"%(i[0]))
            pokemon = cursor.fetchone()[0]
            pokedex.append(pokemon)
        size = len(pokedex)
        size_bytes = size.to_bytes(4, "big")
        connection.send(bytearray([24]))
        if connection.recv(1)[0] == 33:
            connection.send(size_bytes)
        if connection.recv(1)[0] == 33:
            for pokemon in pokedex:
                pokemon_size = len(pokemon).to_bytes(1,"big")
                connection.send(pokemon_size)
                if connection.recv(1)[0] == 33:
                    connection.send(pokemon.encode("utf-8"))
        cerrarSesion(connection)
    except socket.timeout as timeout:
        print("Tiempo de respuesta excedido: 10 segundos")
        avisoTimeout(connection)
        cerrarSesion(connection)
    except IndexError:
        terminarConexion()
    
def muestraCatalogo(connection):
    """Muestra el catalogo.
    
    :param connection: Conexión entre el servidor y el cliente
    :type connection: Conexión
    """
    try:
        cnx = mysql.connect(**CONFIG)
        cursor = cnx.cursor()
        cursor.execute("SELECT Nombre FROM Pokemon")
        result = cursor.fetchall()
        catalogo = []
        for i in result:
            catalogo.append(i[0])
        size = len(catalogo)
        size_bytes = size.to_bytes(4, "big")
        connection.send(bytearray([25]))
        if connection.recv(1)[0] == 33:
            connection.send(size_bytes)
        if connection.recv(1)[0] == 33:
            for pokemon in catalogo:
                pokemon_size = len(pokemon).to_bytes(1,"big")
                connection.send(pokemon_size)
                if connection.recv(1)[0] == 33:
                    connection.send(pokemon.encode("utf-8"))
        cerrarSesion(connection)
    except socket.timeout as timeout:
        print("Tiempo de respuesta excedido: 10 segundos")
        avisoTimeout(connection)
        cerrarSesion(connection)
    except IndexError:
        terminarConexion()

if __name__ == "__main__":
   main()
