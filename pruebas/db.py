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
cursor.execute("SELECT Pokemon FROM Pokedex WHERE Usuario = 5")
result = cursor.fetchall()
pokedex = []
j = 0
for i in result:
	cursor.execute("SELECT Nombre FROM Pokemon WHERE idPokemon = %i"%(i[0]))
	pokemon = cursor.fetchone()[0]
	pokedex.append(pokemon)
	j+=1
for pokemon in pokedex:
	print(pokemon)
#cnx.commit()