CREATE DATABASE IF NOT EXISTS moodflow;
USE moodflow;

CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Sleep_quality (
    Sleep_quality_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    hours_slept DECIMAL(4,2) NOT NULL,
    quality_score INT CHECK (quality_score BETWEEN 1 AND 10),
    dream_intensity INT CHECK (dream_intensity BETWEEN 1 AND 10),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Mood_types (
    mood_type_id INT AUTO_INCREMENT PRIMARY KEY,
    mood_name VARCHAR(50) NOT NULL UNIQUE,
    mood_intensity INT NOT NULL CHECK (mood_intensity BETWEEN 1 AND 10)
);

CREATE TABLE IF NOT EXISTS Recommendation (
    recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
    mood_trigger_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (mood_trigger_id) REFERENCES Mood_types(mood_type_id)
);

CREATE TABLE IF NOT EXISTS User_recommendation (
    user_recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recommendation_id INT NOT NULL,
    date_given TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (recommendation_id) REFERENCES Recommendation(recommendation_id)
);

CREATE TABLE IF NOT EXISTS Recommendation_feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_recommendation_id INT NOT NULL,
    was_helpful BOOLEAN NOT NULL,
    FOREIGN KEY (user_recommendation_id) REFERENCES User_recommendation(user_recommendation_id)
);

CREATE TABLE IF NOT EXISTS Recommendation_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    recommendation_id INT NOT NULL,
    times_given INT DEFAULT 0,
    helpful_count INT DEFAULT 0,
    helpful_rate DECIMAL(5,2) DEFAULT 0.0,
    FOREIGN KEY (recommendation_id) REFERENCES Recommendation(recommendation_id)
);

CREATE TABLE IF NOT EXISTS User_daily_summary (
    summary_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    avg_mood INT DEFAULT 0,
    total_sleep DECIMAL(4,2) DEFAULT 0.0,
    total_steps INT DEFAULT 0,
    avg_stress INT DEFAULT 0 CHECK (avg_stress BETWEEN 1 AND 10),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    UNIQUE (user_id, date)
);

CREATE TABLE IF NOT EXISTS Activity_types (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    activity_name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Activity_log (
    activity_log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    activity_id INT NOT NULL,
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_minutes INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (activity_id) REFERENCES Activity_types(activity_id)
);

CREATE TABLE IF NOT EXISTS Mood_log (
    mood_log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    mood_type_id INT NOT NULL,
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mood_color_hex VARCHAR(7) NOT NULL,
    stress_level INT CHECK (stress_level BETWEEN 1 AND 10),
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (mood_type_id) REFERENCES Mood_types(mood_type_id)
);

CREATE TABLE IF NOT EXISTS Triggers (
    trigger_id INT AUTO_INCREMENT PRIMARY KEY,
    trigger_name VARCHAR(100) NOT NULL,
    trigger_category VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Mood_triggers_bridge (
    mood_log_id INT NOT NULL,
    trigger_id INT NOT NULL,
    PRIMARY KEY (mood_log_id, trigger_id),
    FOREIGN KEY (mood_log_id) REFERENCES Mood_log(mood_log_id),
    FOREIGN KEY (trigger_id) REFERENCES Triggers(trigger_id)
);

CREATE TABLE IF NOT EXISTS Mood_predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    predicted_mood_type_id INT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confidence DECIMAL(5,2) CHECK (confidence BETWEEN 0 AND 10),
    model_version VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (predicted_mood_type_id) REFERENCES Mood_types(mood_type_id)
);

CREATE TABLE IF NOT EXISTS Mood_themes (
    theme_id INT AUTO_INCREMENT PRIMARY KEY,
    mood_type_id INT NOT NULL,
    theme_name VARCHAR(100) NOT NULL,
    background_color_hex VARCHAR(7) NOT NULL,
    accent_color_hex VARCHAR(7) NOT NULL,
    dark_mode_supported BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (mood_type_id) REFERENCES Mood_types(mood_type_id)
);

CREATE TABLE IF NOT EXISTS User_profile (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    preferred_theme_id INT DEFAULT 1,
    age INT,
    gender VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (preferred_theme_id) REFERENCES Mood_themes(theme_id)
);

DROP TABLE IF EXISTS Lifestyle_data;

CREATE TABLE Lifestyle_data (
    lifestyle_id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(100),
    age INT,
    gender VARCHAR(20),
    exercise_level VARCHAR(50),
    diet_type VARCHAR(50),
    sleep_hours FLOAT,
    stress_level FLOAT,
    mental_health_condition VARCHAR(100),
    work_hours_per_week FLOAT,
    screen_time_per_day FLOAT,
    social_interaction_score FLOAT,
    happiness_score FLOAT
);

CREATE TABLE IF NOT EXISTS fitlife_data (
    fitlife_id INT AUTO_INCREMENT PRIMARY KEY,
    date VARCHAR(50),           -- <--- not DATE anymore
    age INT,
    gender VARCHAR(20),
    time_of_day VARCHAR(50),
    activity_category VARCHAR(100),
    sub_category VARCHAR(100),
    activity VARCHAR(100),
    duration_minutes INT,
    intensity VARCHAR(30),
    primary_emotion VARCHAR(50),
    secondary_emotion VARCHAR(50),
    mood_before INT,
    mood_after INT,
    energy_level INT,
    stress_level INT
);

CREATE TABLE IF NOT EXISTS health_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    full_name VARCHAR(100),
    date VARCHAR(20),
    age INT,
    gender VARCHAR(20),
    height_cm FLOAT,
    weight_kg FLOAT,
    steps_taken INT,
    calories_burn FLOAT,
    hours_slept FLOAT,
    water_intake_l FLOAT,
    active_minutes INT,
    heart_rate_bpm INT,
    workout_type VARCHAR(50),
    stress_level INT,
    mood VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS Fitness_Tracking (
    fitness_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    steps INT DEFAULT 0,
    calories INT DEFAULT 0,
    sleep_hours DECIMAL(4,2) DEFAULT 0.0,
    water_intake DECIMAL(4,2) DEFAULT 0.0,
    heart_rate INT DEFAULT 0,
    mood VARCHAR(50) NOT NULL,
    stress_level INT CHECK (stress_level BETWEEN 1 AND 10)
);

CREATE TABLE IF NOT EXISTS Mindfulness_exercises (
    exercise_id INT AUTO_INCREMENT PRIMARY KEY,
    exercise_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    duration_minutes INT NOT NULL,
    difficulty_level INT CHECK (difficulty_level BETWEEN 1 AND 5),
    description TEXT
);

CREATE TABLE IF NOT EXISTS User_exercise_log (
    user_exercise_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    exercise_id INT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed BOOLEAN DEFAULT TRUE,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (exercise_id) REFERENCES Mindfulness_exercises(exercise_id)
);







INSERT INTO Users (username, email, password_hash)
VALUES ('testuser', 'test@example.com', 'abc123');
INSERT INTO Users (username, email, password_hash)
VALUES ('user2', 'user2@example.com', '123');
INSERT INTO Users (username, email, password_hash)
VALUES ('user3', 'user3@example.com', '456');
INSERT INTO Users (username, email, password_hash)
VALUES ('user4', 'user4@example.com', '789');
INSERT INTO Users (username, email, password_hash)
VALUES ('user5', 'user5@example.com', '000');


INSERT INTO Mood_types (mood_name, mood_intensity)
VALUES ('Happy', 7);

SELECT * FROM Users;
SELECT * FROM Mood_types;




ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'Torchlight123!';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;


GRANT ALL PRIVILEGES ON moodflow.* TO 'root'@'%';
FLUSH PRIVILEGES;

SELECT host, user FROM mysql.user;

INSERT INTO Mood_types (mood_name, mood_intensity)
VALUES
('Calm', 5),
('Stressed', 8),
('Sad', 6),
('Angry', 9);
