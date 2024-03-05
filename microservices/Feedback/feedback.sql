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
-- Database: `feedback`
--
CREATE DATABASE IF NOT EXISTS `feedback` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `feedback`;

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
CREATE TABLE IF NOT EXISTS `feedback` (
    `feedbackID` INT AUTO_INCREMENT NOT NULL,
    `backerID` INT NOT NULL,
    `projectID` INT NOT NULL,
    `rating` INT NOT NULL,
    `comment` TEXT NOT NULL,
    `submittedAt` TIMESTAMP NOT NULL,
    `status` ENUM('Pending', 'Approved', 'Rejected') NOT NULL,
    PRIMARY KEY (`feedbackID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`feedbackID`, `backerID`, `projectID`, `rating`, `comment`, `submittedAt`, `status`) VALUES
    (001, 1, 1231, 9, 'excellent', '2024-03-12 11:00:00', 'Approved'),
    (002, 2, 1232, 8, 'good', '2024-03-13 10:00:00', 'Pending'),
    (003, 3, 1233, 7, 'happy', '2024-03-14 11:00:00', 'Approved'),
    (004, 4, 1234, 1, 'shit', '2024-03-15 11:00:00', 'Rejected'),
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;