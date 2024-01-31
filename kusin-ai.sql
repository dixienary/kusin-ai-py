-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 29, 2024 at 10:10 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kusin-ai`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `chat_messages`
--

CREATE TABLE `chat_messages` (
  `message_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `message_text` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `ingredients`
--

CREATE TABLE `ingredients` (
  `ingredient_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `recipes`
--

CREATE TABLE `recipes` (
  `recipe_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `recipe_ingredients`
--

CREATE TABLE `recipe_ingredients` (
  `recipe_id` int(11) NOT NULL,
  `ingredient_id` int(11) NOT NULL,
  `quantity` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `cooking_instructions`
--

CREATE TABLE `cooking_instructions` (
  `instruction_id` int(11) NOT NULL,
  `recipe_id` int(11) NOT NULL,
  `step_number` int(11) NOT NULL,
  `instruction` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Indexes for the tables
--

ALTER TABLE `users` ADD PRIMARY KEY (`user_id`), ADD UNIQUE KEY `email` (`email`);
ALTER TABLE `chat_messages` ADD PRIMARY KEY (`message_id`);
ALTER TABLE `ingredients` ADD PRIMARY KEY (`ingredient_id`);
ALTER TABLE `recipes` ADD PRIMARY KEY (`recipe_id`);
ALTER TABLE `cooking_instructions` ADD PRIMARY KEY (`instruction_id`), ADD KEY `recipe_id` (`recipe_id`);
ALTER TABLE `recipe_ingredients` ADD KEY `recipe_id` (`recipe_id`), ADD KEY `ingredient_id` (`ingredient_id`);

--
-- AUTO_INCREMENT for the tables
--

ALTER TABLE `users` MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
ALTER TABLE `chat_messages` MODIFY `message_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
ALTER TABLE `ingredients` MODIFY `ingredient_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
ALTER TABLE `recipes` MODIFY `recipe_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
ALTER TABLE `cooking_instructions` MODIFY `instruction_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

-- --------------------------------------------------------

--
-- Constraints for the tables
--

ALTER TABLE `cooking_instructions` ADD CONSTRAINT `cooking_instructions_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`recipe_id`);
ALTER TABLE `recipe_ingredients` ADD CONSTRAINT `recipe_ingredients_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`recipe_id`);
ALTER TABLE `recipe_ingredients` ADD CONSTRAINT `recipe_ingredients_ibfk_2` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`ingredient_id`);
--
-- Dumping data for table `cooking_instructions`
--

INSERT INTO `cooking_instructions` (`instruction_id`, `recipe_id`, `step_number`, `instruction`) VALUES
(1, 1, 1, 'In pot over medium heat, heat oil.'),
(2, 1, 2, 'Add onions and garlic and cook, stirring occasionally, until softened.');
(3, 1, 3, 'Add pork and cook until browned.'),
(4, 1, 4, 'Stir in shrimp paste and cook for 2 minutes.'),
(5, 1, 5, 'Pour in coconut milk and bring to a boil.'),
(6, 1, 6, 'Reduce heat to low, cover, and simmer for 20-30 minutes, or until the pork is tender.'),
(7, 1, 7, 'Add green chili, red chili, and ginger. Cook for an additional 5 minutes.'),
(8, 1, 8, 'Season with salt and pepper to taste.'),
(9, 1, 9, 'Serve hot and enjoy your Bicol Express!');
-- --------------------------------------------------------
--
-- Dumping data for table `ingredients`
--

INSERT INTO `ingredients` (`ingredient_id`, `name`) VALUES
(1, 'pork'),
(2, 'coconut milk'),
(3, 'shrimp paste'),
(4, 'garlic'),
(5, 'onion'),
(6, 'ginger'),
(7, 'green chili'),
(8, 'red chili'),
(9, 'salt'),
(10, 'pepper');

-- --------------------------------------------------------
--
-- Dumping data for table `recipes`
--

INSERT INTO `recipes` (`recipe_id`, `name`) VALUES
(1, 'Bicol Express');

-- --------------------------------------------------------
--
-- Dumping data for table `recipe_ingredients`
--

INSERT INTO `recipe_ingredients` (`recipe_id`, `ingredient_id`, `quantity`) VALUES
(1, 1, '2 pounds'),
(1, 2, '1 can (13.5 ounces)'),
(1, 4, '4 cloves'),
(1, 5, '1 large'),
(1, 6, '1-inch piece'),
(1, 7, '2 pieces'),
(1, 9, 'to taste'),
(1, 10, 'to taste');


-- --------------------------------------------------------
--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `email`, `password_hash`) VALUES
(1, 'dixie@email.com', '$2b$12$qRz0fHCXybczHK6vsex5.OaJw.2z6v19FlrbHCYiPjrHHOlmFn5IO');


COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;