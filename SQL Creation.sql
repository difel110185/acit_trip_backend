CREATE DATABASE trippity;

USE trippity;

CREATE TABLE `countries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE countries
ADD CONSTRAINT UI_Countries UNIQUE (name);

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `password` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE users
ADD CONSTRAINT UI_Users UNIQUE (email);

CREATE TABLE `trips` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `image` longtext NOT NULL,
  `country_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_country_idx` (`country_id`),
  CONSTRAINT `fk_country` FOREIGN KEY (`country_id`) REFERENCES `countries` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  KEY `fk_user_idx` (`user_id`),
  CONSTRAINT `fk_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE trips
ADD CONSTRAINT UI_Trips UNIQUE (name);

CREATE TABLE `trip_cities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `datetime_of_arrival` datetime DEFAULT NULL,
  `datetime_of_departure` datetime DEFAULT NULL,
  `trip_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_trips_idx` (`trip_id`),
  CONSTRAINT `fk_trips` FOREIGN KEY (`trip_id`) REFERENCES `trips` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
