-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.32-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.13.0.7147
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para nutrishelf
CREATE DATABASE IF NOT EXISTS `nutrishelf` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `nutrishelf`;

-- Volcando estructura para tabla nutrishelf.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `nombre` varchar(100) NOT NULL,
  `genero` enum('H','M') NOT NULL,
  `fechaNacim` date NOT NULL,
  `actFisica` enum('sedentario','ligera','moderada','alta') NOT NULL,
  `peso` float NOT NULL,
  `altura` float NOT NULL,
  `correo` varchar(500) NOT NULL,
  `passw` varchar(500) NOT NULL,
  PRIMARY KEY (`correo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla nutrishelf.usuarios: ~1 rows (aproximadamente)
REPLACE INTO `usuarios` (`nombre`, `genero`, `fechaNacim`, `actFisica`, `peso`, `altura`, `correo`, `passw`) VALUES
	('Fernando', 'H', '2008-06-18', 'sedentario', 55, 180, 'fer@mail.com', 'scrypt:32768:8:1$lb979yQ8lBTSKyhK$6296539062cc14376b5f49d3257d9738e489bc6ae7de47015f5cc6b60111c673292a30ef9c204d19731401bb212c0029af0593a5e0674ef7ddb01642f6f3c65f');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
