USE sql12662061;

CREATE TABLE IF NOT EXISTS test_table(
        id INT PRIMARY KEY AUTO_INCREMENT,
        test_field VARCHAR(250) NOT NULL DEFAULT ''
); 


#INSERT INTO test_table(test_field) VALUES('test1');
INSERT INTO test_table(test_field) VALUES('test2');

