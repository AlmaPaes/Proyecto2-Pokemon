# Códigos de Mensajes

1. Códigos del cliente (10)
   - 10: Solicitar al servidor por parte del cliente, un Pokemon para capturar. 
   - 11: Solicita ver el catalogo y su pokedex. 
   - 12: Regresar al inicio de la conexión.
2. Códigos del servidor (20)
   - 20: ¿Capturar al Pokemon x?.
   - 21: ¿Intentar captura de nuevo? Quedan k intentos.
   - 22: Envía Pokemon (imagen) capturado.
   - 23: Número de intentos de captura agotados.
   - 24: Envía pokedex y catálogo.
3. Códigos en común (30):
   - 30: Sí
   - 31: No
   - 32: Terminando conexión
   - 33: Ack/Recibido
4. Códigos de error (40):
   - 40: Se rechaza la solicitud de conexión
   - 41: Se cierra la conexión por timeout. Espera finalizada.

### <u>Mensajes:</u>

Definimos el contenido de cada mensaje de la siguiente manera, tomando en cuenta que cada mensaje respetará el tamaño indicado en el PDF.

- 1 byte:
  - 10: "P"



## Nuevos Estados

- S8: El servidor recibe la solicitud de ver catálogo de pokemones. Y lo envía.
- S9: El cliente recibe el catálogo de pokemones.

