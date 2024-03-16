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
-- Database: `project`
--
CREATE DATABASE IF NOT EXISTS `project` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `project`;

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `project`;
CREATE TABLE IF NOT EXISTS `project` (
    `project_id` INT AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `creator_id` VARCHAR(255) NOT NULL,
    `funding_goal` INT NOT NULL,
    `deadline` DATETIME NOT NULL,
    `creation_time` TIMESTAMP NOT NULL,
    `status` VARCHAR(255) NOT NULL,
    `goal_reached` BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `project`
--

INSERT INTO `project` (`project_id`, `name`, `description`, `creator_id`, `funding_goal`, `deadline`, `creation_time`, `status`, `goal_reached`) VALUES
    (1231, 'Project A', 'Description for Project A', 'Creator1', 5000, '2024-03-31 12:00:00', '2024-01-31 11:00:00', 'Open', FALSE),
    (1232, 'Project B', 'Description for Project B', 'Creator2', 10000, '2024-04-15 18:30:00', '2024-01-31 10:00:00', 'Open', FALSE),
    (1233, 'Project C', 'Description for Project C', 'Creator3', 7500, '2024-05-20 09:45:00', '2024-01-31 9:00:00', 'Open', FALSE),
    (1234, 'Project D', 'Description for Project D', 'Creator4', 12000, '2024-06-10 15:15:00', '2024-01-31 3:00:00', 'Open', FALSE);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;