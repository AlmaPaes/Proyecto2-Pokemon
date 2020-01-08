CREATE DATABASE `TCP201-Pokemon`;

USE `TCP201-Pokemon`;

/*Install Pokemon Table*/

DROP TABLE IF EXISTS `Pokemon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pokemon` (
  `idPokemon` int(10) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(45) NOT NULL,
  PRIMARY KEY (`idPokemon`),
  UNIQUE KEY `idPokemon_UNIQUE` (`idPokemon`)
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pokemon`
--

LOCK TABLES `Pokemon` WRITE;
/*!40000 ALTER TABLE `Pokemon` DISABLE KEYS */;
INSERT INTO `Pokemon` VALUES (1,'Bulbasaur'),(2,'Ivysaur'),(3,'Venusaur'),(4,'Charmander'),(5,'Charmeleon'),(6,'Charizard'),(7,'Squirtle'),(8,'Wartortle'),(9,'Blastoise'),(10,'Caterpie'),(11,'Metapod'),(12,'Butterfree'),(13,'Weedle'),(14,'Kakuna'),(15,'Beedrill'),(16,'Pidgey'),(17,'Pidgeotto'),(18,'Pidgeot'),(19,'Rattata'),(20,'Raticate'),(21,'Spearow'),(22,'Fearow'),(23,'Ekans'),(24,'Arbok'),(25,'Pikachu'),(26,'Raichu'),(27,'Sandshrew'),(28,'Sandslash'),(29,'Nidoran (female)'),(30,'Nidorina'),(31,'Nidoqueen'),(32,'Nidoran (male)'),(33,'Nidorino'),(34,'Nidoking'),(35,'Clefairy'),(36,'Clefable'),(37,'Vulpix'),(38,'Ninetales'),(39,'Jigglypuff'),(40,'Wigglytuff'),(41,'Zubat'),(42,'Golbat'),(43,'Oddish'),(44,'Gloom'),(45,'Vileplume'),(46,'Paras'),(47,'Parasect'),(48,'Venonat'),(49,'Venomoth'),(50,'Diglett'),(51,'Dugtrio'),(52,'Meowth'),(53,'Persian'),(54,'Psyduck'),(55,'Golduck'),(56,'Mankey'),(57,'Primeape'),(58,'Growlithe'),(59,'Arcanine'),(60,'Poliwag'),(61,'Poliwhirl'),(62,'Poliwhrath'),(63,'Abra'),(64,'Kadabra'),(65,'Alakazam'),(66,'Machop'),(67,'Machoke'),(68,'Machamp'),(69,'Bellsprout'),(70,'Weepinbell'),(71,'Victreebel'),(72,'Tentacool'),(73,'Tentacruel'),(74,'Geodude'),(75,'Graveler'),(76,'Golem'),(77,'Ponyta'),(78,'Rapidash'),(79,'Slowpoke'),(80,'Slowbro'),(81,'Magnemite'),(82,'Magneton'),(83,'Farfetchd'),(84,'Doduo'),(85,'Dodrio'),(86,'Seel'),(87,'Dewgong'),(88,'Grimer'),(89,'Mulk'),(90,'Shellder'),(91,'Cloyster'),(92,'Gastly'),(93,'Haunter'),(94,'Gengar'),(95,'Onix'),(96,'Drowzee'),(97,'Hypno'),(98,'Krabby'),(99,'Kingler'),(100,'Voltorb'),(101,'Electrode'),(102,'Exeggcute'),(103,'Exeggutor'),(104,'Cubone'),(105,'Marowak'),(106,'Hitmonlee'),(107,'Hitmonchan'),(108,'Lickitung'),(109,'Koffing'),(110,'Weezing'),(111,'Rhyhorn'),(112,'Rhydon'),(113,'Chansey'),(114,'Tangela'),(115,'Kangaskhan'),(116,'Horsea'),(117,'Seadra'),(118,'Goldeen'),(119,'Seaking'),(120,'Staryu'),(121,'Starmie'),(122,'Mr. Mime'),(123,'Scyther'),(124,'Jynx'),(125,'Electabuzz'),(126,'Magmar'),(127,'Pinsir'),(128,'Tauros'),(129,'Magikarp'),(130,'Gyarados'),(131,'Lapras'),(132,'Ditto'),(133,'Eevee'),(134,'Vaporeon'),(135,'Jolteon'),(136,'Flareon'),(137,'Polygon'),(138,'Omanyte'),(139,'Omastar'),(140,'Kabuto'),(141,'Kabutops'),(142,'Aerodactyl'),(143,'Snorlax'),(144,'Articuno'),(145,'Zapdos'),(146,'Moltres'),(147,'Dratini'),(148,'Dragonair'),(149,'Dragonite'),(150,'Mewtwo');


/*!40000 ALTER TABLE `Pokemon` ENABLE KEYS */;
UNLOCK TABLES;


/*Install Usuario Table*/

DROP TABLE IF EXISTS `Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Usuario` (
  `idUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(45) NOT NULL,
  `Pwd` varchar(16) NOT NULL,
  PRIMARY KEY (`idUsuario`),
  UNIQUE KEY `idUsuario_UNIQUE` (`idUsuario`),
  UNIQUE KEY `Nombre_UNIQUE` (`Nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario`
--

LOCK TABLES `Usuario` WRITE;
/*!40000 ALTER TABLE `Usuario` DISABLE KEYS */;
INSERT INTO `Usuario` VALUES (1,'Alma','doggos2020'),(2,'Paulo','profesor'),(3,'Ismael','ayudante.lab'),(4,'Ulises','ayudante.clase'),(5,'Alejandro','doggos2020');
/*!40000 ALTER TABLE `Usuario` ENABLE KEYS */;
UNLOCK TABLES;

/*Install Pokedex Table*/

DROP TABLE IF EXISTS `Pokedex`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pokedex` (
  `idPokedex` int(11) NOT NULL AUTO_INCREMENT,
  `Usuario` int(11) NOT NULL,
  `Pokemon` int(11) NOT NULL,
  PRIMARY KEY (`idPokedex`),
  UNIQUE KEY `idPokedex_UNIQUE` (`idPokedex`),
  KEY `Usuario_idx` (`Usuario`),
  KEY `Pokemon_idx` (`Pokemon`),
  CONSTRAINT `Pokemon` FOREIGN KEY (`Pokemon`) REFERENCES `Pokemon` (`idPokemon`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Usuario` FOREIGN KEY (`Usuario`) REFERENCES `Usuario` (`idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pokedex`
--

LOCK TABLES `Pokedex` WRITE;
/*!40000 ALTER TABLE `Pokedex` DISABLE KEYS */;
INSERT INTO `Pokedex` VALUES (1,5,77),(2,5,113),(3,5,144),(4,5,21);
/*!40000 ALTER TABLE `Pokedex` ENABLE KEYS */;
UNLOCK TABLES;
