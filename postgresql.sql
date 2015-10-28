CREATE DATABASE "company";

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(40) NOT NULL,
    lastname VARCHAR(40) NOT NULL,
    username VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL,
    imei VARCHAR(20) NOT NULL,
    created TIMESTAMP NOT NULL,
    modified TIMESTAMP
);

CREATE TABLE ping(
    id SERIAL PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    created TIMESTAMP NOT NULL,
    modified TIMESTAMP
);