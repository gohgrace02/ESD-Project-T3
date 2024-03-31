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
-- Database: `error`
--
CREATE DATABASE IF NOT EXISTS `error` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `error`;

-- --------------------------------------------------------

--
-- Table structure for table `error`
--

DROP TABLE IF EXISTS `error`;
CREATE TABLE IF NOT EXISTS `error` (
    `log_id` INT AUTO_INCREMENT NOT NULL,
    `code` INT NOT NULL,
    `data` VARCHAR(255) NOT NULL,
    `message` VARCHAR(255) NOT NULL,
    `microservice` VARCHAR(255) NOT NULL,

    PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `error`
--

INSERT INTO `error` (`log_id`, `code`, `data`, `message`, `microservice`) VALUES
    (1, 400, "{'name': 'Project A', 'description': 'Stupid thing', 'creator_id': 'Creator1', 'funding_goal': 5000, 'deadline': '2024-04-15 18:30:00', 'status': 'Open', 'goal_reached': False}", 'Vetting is unsuccessful. Project not created.', 'vetting'),
    (2, 400, 'stupid project', 'Moderation is unsuccessful. Feedback not posted.', 'moderation');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;