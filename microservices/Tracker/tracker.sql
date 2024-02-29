-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tracker`
--
CREATE DATABASE IF NOT EXISTS `tracker` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `tracker`;

-- --------------------------------------------------------

--
-- Table structure for table `tracker`
--

DROP TABLE IF EXISTS `tracker`;
CREATE TABLE IF NOT EXISTS `tracker` (
    `trackerID` INT AUTO_INCREMENT NOT NULL,
    `backerID` INT NOT NULL,
    `projectID` INT NOT NULL,
    `pledgeAmt` FLOAT NOT NULL,
    PRIMARY KEY (`trackerID`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- NEED TO ADD THIS IN THE FUTURE
-- FOREIGN KEY (`backerID`) REFERENCES `Backer`(`backerID`),
-- FOREIGN KEY (`projectID`) REFERENCES `Project`(`projectID`)

--
-- Dumping data for table `tracker`
--

INSERT INTO `Tracker` (`backerID`, `projectID`, `pledgeAmt`) VALUES
    (1, 1, 100.00),
    (2, 1, 50.00),
    (3, 2, 75.00),
    (4, 3, 200.00),
    (5, 4, 150.00);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;