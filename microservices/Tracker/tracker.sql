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
    `tracker_id` INT AUTO_INCREMENT NOT NULL,
    `backer_id` INT NOT NULL,
    `project_id` INT NOT NULL,
    `pledge_amt` FLOAT NOT NULL,
    `payment_intent_id` VARCHAR(255) NOT NULL,
    `captured` BOOLEAN,
    PRIMARY KEY (`tracker_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- NEED TO ADD THIS IN THE FUTURE
-- FOREIGN KEY (`backer_id`) REFERENCES `Backer`(`backer_id`),
-- FOREIGN KEY (`project_id`) REFERENCES `Project`(`project_id`)

--
-- Dumping data for table `tracker`
--

INSERT INTO `Tracker` (`backer_id`, `project_id`, `pledge_amt`, `payment_intent_id`) VALUES
    (1, 1236, 20.00, 'pi_3OzlB6BWraf69XnW1CHBs7KW'),
    (2, 1236, 20.00, 'pi_3OzlJGBWraf69XnW1pNmRiBH'),
    (3, 1236, 20.00, 'pi_3OzlKRBWraf69XnW1TeuPryG'),
    (4, 1236, 20.00, 'pi_3OzlKoBWraf69XnW1G8GM5bl');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;