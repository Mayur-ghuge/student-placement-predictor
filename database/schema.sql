CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100),
    department VARCHAR(100),
    cgpa DECIMAL(4,2),
    aptitude_score INT,
    communication_score INT,
    coding_score INT,
    projects INT,
    internships INT,
    backlogs INT,
    probability DECIMAL(5,2),
    prediction_result VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);