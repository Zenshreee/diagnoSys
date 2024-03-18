import os
import json

# DROP TABLE IF EXISTS episodes;

# CREATE TABLE episodes(
#     id int,
#     title varchar(64),
#     descr varchar(1024)
# );


def json_to_sql(path: str) -> None:
    with open(path, "r") as file:
        adverse_to_webster = json.load(file)

    with open("../resources/init.sql", "a") as file:
        file.write(f"""CREATE DATABASE  IF NOT EXISTS `definitions_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `definitions_db`;
-- MySQL dump 10.13  Distrib 8.0.31, for macos12 (x86_64)
--
-- Host: localhost    Database: atlas_data
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
-- Table structure for table `atlas_data`
--

DROP TABLE IF EXISTS `atlas_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `atlas_data` (
  `index` int DEFAULT NULL,
  `attraction` text,
  `location` text,
  `blurb` text,
  `url` text,
  `description` text,
  `tags` text,
  `lemmatized_description` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `atlas_data`
--
                   
                   """)
        file.write(f"DROP TABLE IF EXISTS definitions\n\n")
        file.write(f"CREATE TABLE definitions(\n")
        file.write(f"\tid int,\n")
        file.write(f"\ttitle varchar(64)\n")
        file.write(f"\tdescr varchar(1024)\n);\n\n")

    for adverse, description in adverse_to_webster.items():

        with open("../resources/init.sql", "a") as file:
            file.write(
                f"INSERT INTO definitions VALUE(1,'{adverse}','{description}')\n"
            )
    
    return None

if __name__ == '__main__':
    json_to_sql("/definitions.json")
