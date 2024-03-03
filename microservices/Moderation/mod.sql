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
CREATE DATABASE IF NOT EXISTS `mod` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `mod`;

-- --------------------------------------------------------

--
-- Table structure for table `tracker`
--

DROP TABLE IF EXISTS `mnod`;
CREATE TABLE IF NOT EXISTS `mod` (
    `moderationID` INT AUTO_INCREMENT NOT NULL,
    `comment` TEXT NOT NULL,
    `actionTaken` TEXT NOT NULL,
    `reason` TEXT NOT NULL,
    `moderatedAt` TIMESTAMP NOT NULL,
    PRIMARY KEY (`moderationID`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- MAYBE I ALSO??? COPY FROM GRACE ONE 
-- NEED TO ADD THIS IN THE FUTURE
-- FOREIGN KEY (`backerID`) REFERENCES `Backer`(`backerID`),
-- FOREIGN KEY (`projectID`) REFERENCES `Project`(`projectID`)

--
-- Dumping data for table `mod`
--

INSERT INTO `mod` (`moderationID`, `comment`, `actionTaken`, `reason`, `moderatedAt`) VALUES
    (001, 'excellent', 'Approved', 'NIL', '2024-03-12 11:00:00'),
    (002, 'happy', 'Approved', 'NIL', '2024-03-14 11:00:00'),
    (003, 'shit', 'Rejected', 'Vulgarity Spotted', '2024-03-15 11:00:00'),
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;