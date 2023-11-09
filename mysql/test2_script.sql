USE sql12659958;

CREATE TABLE test_table2(
        3id INT PRIMARY KEY AUTO_INCREMENT,
        3test_field VARCHAR(250) NOT NULL DEFAULT ''
);


INSERT INTO test_table2(test_field) VALUES('test1');
INSERT INTO test_table2(test_field) VALUES('test2');
INSERT INTO test_table2(test_field) VALUES('test3');
