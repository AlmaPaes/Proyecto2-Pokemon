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

    - Pasos previos para instalar la base de datos. Revisar archivo.
    
    - En una terminal, nos situamos en la ubicación del archivo *pokemonServer.py*
    
    - Para que se pueda establecer la comunicación satisfactoriamente, necesitamos ingresar la dirección IP al momento de iniciar el servidor. Por lo tanto, ejecutamos *./pokemonServer.py <IP>*
    
* Para el cliente

    - En una terminal, nos situamos en la ubicación del archivo *pokemonClient.py*
    
    - Este programa recibe como parámetros iniciales la dirección IP a través de la cual se quiere conectar, y el puerto. Por lo tanto, ejecutamos de la siguiente manera: *./pokemonClient.py <IP> <port>*
    
.. note :: La dirección IP ingresada al ejecutar el cliente y el servidor debe ser la misma

Programas involucrados
========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   pokemonClient
   pokemonServer
   

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
