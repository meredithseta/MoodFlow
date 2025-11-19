CREATE TABLE test_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255)
);

INSERT INTO test_table (message)
VALUES ('MoodFlow Checkpoint 1 Demo Successful');

SELECT * FROM test_table;
