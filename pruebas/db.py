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
cursor.execute("SELECT idUsuario FROM Usuario WHERE Nombre = %s"%(user))
print(cursor.fetchone()[0])
#cnx.commit()