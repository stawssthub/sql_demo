CREATE DATABASE db_test;

USE db_test;

CREATE TABLE customer (
  id INT,
  custname VARCHAR(100)
);

INSERT INTO customer (id, custname) VALUES
(4, 'ABC Co'),
(2, 'XYZ Corp'),
(3, 'BN Plumbing');
