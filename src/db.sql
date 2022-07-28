CREATE TABLE `Users` (
  `email` varchar(255) NOT NULL,
  `password` binary(64) NOT NULL,
  UNIQUE KEY `email` (`email`)
);