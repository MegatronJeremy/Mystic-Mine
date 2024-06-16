DROP DATABASE IF EXISTS courier_service_database;
CREATE DATABASE courier_service_database;
USE courier_service_database;

DROP TABLE IF EXISTS couriers;
DROP TABLE IF EXISTS packages;
DROP TABLE IF EXISTS deliveries;

CREATE TABLE packages (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    description varchar(256) NOT NULL,
    delivery_price int NOT NULL,
    arrival_date datetime NOT NULL
);

CREATE TABLE couriers (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email varchar ( 256 ) NOT NULL UNIQUE,
    forename varchar( 256 ) NOT NULL,
    surname varchar( 256 ) NOT NULL
);

CREATE TABLE deliveries (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    contract_address varchar(64) DEFAULT NULL,
    package_id int NOT NULL,
    courier_id int NOT NULL,
    FOREIGN KEY ( courier_id ) REFERENCES couriers ( id ),
    FOREIGN KEY ( package_id ) REFERENCES packages ( id )
);