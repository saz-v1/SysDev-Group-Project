-- MySQL dump 10.13  Distrib 8.0.33, for macos13 (arm64)
--
-- Host: 127.0.0.1    Database: horizon
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu` (
  `menu_id` int NOT NULL AUTO_INCREMENT,
  `menu_name` varchar(150) DEFAULT NULL,
  `menu_type` enum('Main','Drink','Dessert') DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`menu_id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
INSERT INTO `menu` VALUES (1,'Deep Dish Pizza','Main',20.00),(2,'NYC Pizza','Main',11.99),(3,'Grilled Salmon Fillet','Main',15.99),(4,'Milk','Drink',18.99),(5,'Spaghetti Carbonara','Main',10.99),(6,'Fish and Chips','Main',11.99),(7,'Lasagna','Main',13.99),(8,'Chicken Parmesan','Main',14.99),(9,'Vegetable Stir Fry','Main',9.99),(10,'Beef Burger','Main',10.99),(11,'Gin and Tonic','Drink',6.99),(13,'Mojito','Drink',7.99),(14,'Virgin Pina Colada','Drink',5.99),(15,'Coca-Cola','Drink',2.49),(16,'Sprite','Drink',2.49),(17,'Fanta','Drink',2.49),(18,'Dr Pepper','Drink',2.49),(19,'Lemonade','Drink',3.49),(20,'Iced Tea','Drink',3.99),(21,'Champagne','Drink',25.99),(22,'White Wine','Drink',15.99),(23,'Red Wine','Drink',16.99),(24,'Whiskey','Drink',8.99),(25,'Vodka','Drink',7.99),(26,'Gin & Juice','Drink',40.99),(27,'Tequila','Drink',9.99),(28,'Tiramisu','Dessert',7.99),(29,'Key Lime Pie','Dessert',6.99),(30,'Lime & soda','Drink',10.00),(31,'Cheesecake','Dessert',5.99),(33,'alize and cristal','Drink',350.00),(38,'Fried Rice','Main',20.00),(41,'Shepherd\'s pie','Main',20.00);
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-22  3:57:04
