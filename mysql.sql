CREATE DATABASE IF NOT EXISTS `company`;

USE `company`;

/*CREATE USER 'company-user'@'localhost' IDENTIFIED BY 'company-user';
GRANT ALL PRIVILEGES ON `company`.* TO 'company-user'@'localhost';
FLUSH PRIVILEGES;*/

CREATE TABLE IF NOT EXISTS users(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(40) NOT NULL,
    lastname VARCHAR(40) NOT NULL,
    username VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL,
    imei VARCHAR(20) NOT NULL,
    created TIMESTAMP NOT NULL,
    modified TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS ping(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    created TIMESTAMP NOT NULL,
    modified TIMESTAMP NOT NULL
);