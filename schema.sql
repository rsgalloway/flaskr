DROP TABLE IF EXISTS `entries`;
CREATE TABLE `entries` (
  `id` int(25) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `text` text NOT NULL,
  PRIMARY KEY `id` (`id`)
);
