.. Proyecto2-Pokemon documentation master file, created by
   sphinx-quickstart on Mon Dec  9 01:13:05 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pokemon Go!
***********
   
.. note :: Bienvenido a la documentación del Proyecto 2 de la materia de Redes de Computadoras

¿Cómo usar?
===========

.. note :: Primero inicializamos el servidor, y después los clientes pueden iniciar una conexión

* Para el servidor

    - Si es la primera vez usando el servidor del juego, por favor dirigirse a la carpeta *./Instalaciones* y ejecutar *./make_servidor*
    
    - En caso contrario: en una terminal, nos situamos en la ubicación del archivo *pokemonServer.py*
    
    - No necesitamos parámetros extra para ejecutar el servidor. *./pokemonServer.py*
    
* Para el cliente

    - Si es la primera vez usando un cliente del juego, por favor dirigirse a la carpeta *./Instalaciones* y ejecutar *./make_cliente*

    - En una terminal, nos situamos en la ubicación del archivo *pokemonClient.py*
    
    - Este programa recibe como parámetros iniciales la dirección IP a través de la cual se quiere conectar, y el puerto. Por lo tanto, ejecutamos de la siguiente manera: *./pokemonClient.py <IP> <port>*
    
.. note :: El puerto ingresado al ejecutar el cliente debe ser el mismo que usa el servidor

Programas involucrados
========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   pokemonClient
   pokemonServer
   
