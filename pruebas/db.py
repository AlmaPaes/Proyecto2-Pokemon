import mysql.connector as mysql

config = {
  'user': 'doggos',
  'password': 'doggos2020',
  'host': 'localhost',
  'database': 'TPC201-Pokemon',
  'raise_on_warnings': True
}

cnx = mysql.connect(**config)
cursor = cnx.cursor()
#cursor.execute("""INSERT INTO Pokedex (Usuario, Pokemon) VALUES (5, 135)""")
user = "Ismael"
user = "'%s'" % user
idPokemon = 100
cursor.execute("SELECT idUsuario FROM Usuario WHERE Nombre = %s"%(user))
idUser = cursor.fetchone()[0]
cursor.execute("INSERT INTO Pokedex (Usuario, Pokemon) VALUES (%i, %i)"%(idUser,idPokemon))
cnx.commit() # guardar el insert into

#Mostrar pokedex|catalogo
"""cursor.execute("SELECT Pokemon FROM Pokedex WHERE Usuario = 5")
result = cursor.fetchall()
pokedex = []
for i in result:
	cursor.execute("SELECT Nombre FROM Pokemon WHERE idPokemon = %i"%(i[0]))
	pokemon = cursor.fetchone()[0]
	pokedex.append(pokemon)
for col1,col2 in zip(pokedex[::2],pokedex[1::2]):
	print(col1+",",col2+",")
print("\n\n")
cursor.execute("SELECT Nombre FROM Pokemon")
result = cursor.fetchall()
catalogo = []
for i in result:
	catalogo.append(i[0])
for col1,col2,col3,col4,col5,col6 in zip(catalogo[::6],catalogo[1::6],catalogo[2::6],catalogo[3::6],catalogo[4::6],catalogo[5::6]):
	print (col1+",",col2+",",col3+",",col4+",",col5+",",col6+",")"""
