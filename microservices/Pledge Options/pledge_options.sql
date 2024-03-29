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
--
-- Database: `project`
--
CREATE DATABASE IF NOT EXISTS `pledge_options` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pledge_options`;


-- --------------------------------------------------------


--
-- Table structure for table `pledge_options`
--


DROP TABLE IF EXISTS `pledge_options`;
CREATE TABLE IF NOT EXISTS `pledge_options` (
    `option_id` INT AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `creator_id` VARCHAR(255) NOT NULL,
    `project_id` INT NOT NULL,
    `pledge_amt` INT NOT NULL,
    `price_id` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`option_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Dumping data for table `project`
--


INSERT INTO `pledge_options` (`option_id`, `title`, `description`, `creator_id`, `project_id`, `pledge_amt`, `price_id`) VALUES
    (1, 'Gold Tier', 'Lorem ipsum dolor sit amet consectetur adipisicing elit.', 'Creator1', 1231, '1000', 'price_1OzXtuBWraf69XnWOJIEupXh');
COMMIT;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;