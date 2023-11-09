USE sql12659958;

CREATE TABLE test_table5(
        id INT PRIMARY KEY AUTO_INCREMENT,
        test_field VARCHAR(250) NOT NULL DEFAULT ''
);


INSERT INTO test_table5(test_field) VALUES('test1');
INSERT INTO test_table5(test_field) VALUES('test2');
INSERT INTO test_table5(test_field) VALUES('test4');
