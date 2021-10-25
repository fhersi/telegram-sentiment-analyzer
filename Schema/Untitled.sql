CREATE TABLE `users`
(
  `uid` int PRIMARY KEY,
  `t_id` int UNIQUE NOT NULL,
  `username` varchar(255),
  `first_name` varchar(255),
  `last_name` varchar(255),
  `created_at` varchar(255)
);

CREATE TABLE `projects`
(
  `pid` int PRIMARY KEY,
  `name` varchar(255) UNIQUE NOT NULL,
  `label` ENUM ('payment', 'utility', 'privacy', 'stablecoins', 'blockchains'),
  `members` int
);

CREATE TABLE `groups`
(
  `uid` int NOT NULL,
  `pid` int NOT NULL,
  `s_date` date NOT NULL
);

ALTER TABLE `users` ADD FOREIGN KEY (`uid`) REFERENCES `groups` (`uid`);

ALTER TABLE `projects` ADD FOREIGN KEY (`pid`) REFERENCES `groups` (`pid`);
