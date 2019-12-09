-- MySQL dump 10.13  Distrib 5.7.28, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: TPC201-Pokemon
-- ------------------------------------------------------
-- Server version	5.7.28-0ubuntu0.18.04.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Pokemon`
--

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

\q

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

/*-- Dump completed on 2019-12-09 10:46:01*/
