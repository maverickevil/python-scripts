DROP DATABASE `blog`;
DROP DATABASE
IF
	EXISTS `blog`;
CREATE DATABASE `blog` DEFAULT charset utf8 COLLATE utf8_general_ci;
USE `blog`;

CREATE TABLE `blog`.`user` (
	id INT NOT NULL auto_increment PRIMARY KEY,
	username VARCHAR ( 16 ) NOT NULL,
	nickname VARCHAR ( 16 ) NOT NULL,
	mobile CHAR ( 11 ) NOT NULL,
	PASSWORD VARCHAR ( 64 ) NOT NULL,
	email VARCHAR ( 64 ) NOT NULL,
	ctime DATETIME NOT NULL
) DEFAULT charset = utf8;

CREATE TABLE `blog`.`article` (
	id INT NOT NULL auto_increment PRIMARY KEY,
	title VARCHAR ( 255 ) NOT NULL,
	TEXT TEXT NOT NULL,
	read_count INT DEFAULT 0,
	comment_count INT DEFAULT 0,
	up_count INT DEFAULT 0,
	down_count INT DEFAULT 0,
	user_id INT NOT NULL,
	ctime DATETIME NOT NULL,
	CONSTRAINT fk_article_user FOREIGN KEY ( user_id ) REFERENCES `blog`.`user` ( id )
) DEFAULT charset = utf8;

CREATE TABLE `blog`.`comment` (
	id INT NOT NULL auto_increment PRIMARY KEY,
	content VARCHAR ( 255 ) NOT NULL,
	user_id INT NOT NULL,
	article_id INT NOT NULL,
	ctime DATETIME NOT NULL,
	CONSTRAINT fk_comment_user FOREIGN KEY ( user_id ) REFERENCES `blog`.`user` ( id ),
	CONSTRAINT fk_comment_article FOREIGN KEY ( article_id ) REFERENCES `blog`.`article` ( id )
) DEFAULT charset = utf8;

CREATE TABLE `blog`.`up_down` (
	id INT NOT NULL auto_increment PRIMARY KEY,
	choice TINYINT NOT NULL,
	user_id INT NOT NULL,
	article_id INT NOT NULL,
	ctime DATETIME NOT NULL,
	CONSTRAINT fk_up_down_user FOREIGN KEY ( user_id ) REFERENCES `blog`.`user` ( id ),
CONSTRAINT fk_up_down_article FOREIGN KEY ( article_id ) REFERENCES `blog`.`article` ( id )
) DEFAULT charset = utf8;
