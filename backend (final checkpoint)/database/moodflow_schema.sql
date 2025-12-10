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
    sleep_quality_id INT AUTO_INCREMENT PRIMARY KEY,
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

CREATE TABLE IF NOT EXISTS Lifestyle_data (
    lifestyle_id INT AUTO_INCREMENT PRIMARY KEY,
    age_group VARCHAR(20) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    sleep_hours_avg DECIMAL(4,2) DEFAULT 0.0,
    exercise_frequency INT DEFAULT 0, -- times per week
    diet_quality_score INT DEFAULT 0 CHECK (diet_quality_score BETWEEN 1 AND 10),
    happiness_index INT DEFAULT 0 CHECK (happiness_index BETWEEN 1 AND 10),
    stress_level INT DEFAULT 0 CHECK (stress_level BETWEEN 1 AND 10)
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

CREATE TABLE IF NOT EXISTS Audit_log (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(255) NOT NULL,
    table_name VARCHAR(100),
    record_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);