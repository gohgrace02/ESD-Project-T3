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
    `product_id` VARCHAR(255) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `user_id` INT NOT NULL,
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


INSERT INTO `project` (`project_id`,`product_id`, `name`, `description`, `user_id`, `funding_goal`, `deadline`, `creation_time`, `status`, `goal_reached`) VALUES
    (1231, 'prod_PpCDC2PwIfSJEJ', 'Home Gardening System', "A smart gardening system that allows users to effortlessly grow herbs, vegetables, or flowers indoors. This system includes automated watering, LED grow lights with adjustable spectra, and sensors to monitor soil moisture, temperature, and sunlight exposure. Users could control the system remotely via a mobile app, receive notifications and tips for plant care, and track the growth progress of their plants.
", '2', 5000, '2024-03-31 12:00:00', '2024-01-31 11:00:00', 'Open', FALSE),

    (1232, 'prod_PpIgZpNc1uWRbq', 'Smart Home Security Hub', "An intelligent home security hub that goes beyond traditional security systems. This hub incorporates features such as facial recognition technology, smart doorbell integration, and AI-powered anomaly detection to identify potential security threats. It also offers emergency response coordination, integration with third-party security services, and real-time alerts to users' smartphones.
", '2', 10000, '2024-04-15 18:30:00', '2024-01-31 10:00:00', 'Open', FALSE),

    (1233, 'prod_PpIgB4T9XwaMMY', 'Smart Pet Care System', "A smart pet care system that helps pet owners monitor and care for their furry companions remotely. This system includes features such as automatic pet feeders, interactive toys, and video monitoring cameras with two-way audio communication. It could also offer activity tracking, health monitoring, and personalized recommendations for pet care based on breed, age, and activity level.", '2', 7500, '2024-05-20 09:45:00', '2024-01-31 9:00:00', 'Open', FALSE),

    (1234, 'prod_PpIg4PmC0uun8j', 'Delicious Cat Food', "MEOWMEOEWMEOWMEOEWMOWEMOEWEWMEOW", '4', 12000, '2024-06-10 15:15:00', '2024-01-31 3:00:00', 'Open', FALSE);
COMMIT;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;