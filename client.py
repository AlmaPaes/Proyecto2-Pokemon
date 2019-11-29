import socket
import sys
def main():
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   host = "127.0.0.1"
   port = 9999
   try:
      s.connect((host, port))
   except:
      print("Connection Error")
      sys.exit()
   message = input("Deseas capturar un Pokemon?\n -> ")
   while message != 'quit':
      s.send(message.encode("utf8"))
      print("Quieres capturar a " + 
            getPokemon(s.recv(5120).decode("utf8")) + "?")
      #if s.recv(5120).decode("utf8") == "-":
      #   pass # null operation
      message = input(" -> ")
   s.send(b'--quit--')

def getPokemon(message):
   if(message[0:2] == "20"):
      return message[-1]
   else:
      return "Error"

if __name__ == "__main__":
   main()