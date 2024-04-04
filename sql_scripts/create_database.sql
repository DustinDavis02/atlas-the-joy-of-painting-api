-- Creating the Database
CREATE DATABASE IF NOT EXISTS JoyOfPaintingDB;
USE JoyOfPaintingDB;

-- Creating the Episodes Table
CREATE TABLE IF NOT EXISTS Episodes (
    EpisodeID VARCHAR(10) PRIMARY KEY,
    Title VARCHAR(255),
    SeasonNumber INT,
    EpisodeNumber INT,
    AirDate DATE
);

-- Creating the Colors Table
CREATE TABLE IF NOT EXISTS Colors (
    ColorID INT AUTO_INCREMENT PRIMARY KEY,
    ColorName VARCHAR(50),
    ColorHexCode VARCHAR(7)
);

-- Creating the SubjectMatter Table
CREATE TABLE IF NOT EXISTS SubjectMatter (
    SubjectID INT AUTO_INCREMENT PRIMARY KEY,
    SubjectName VARCHAR(255)
);

-- Creating the EpisodeColors Junction Table
CREATE TABLE IF NOT EXISTS EpisodeColors (
    EpisodeID VARCHAR(10),
    ColorID INT,
    FOREIGN KEY (EpisodeID) REFERENCES Episodes(EpisodeID),
    FOREIGN KEY (ColorID) REFERENCES Colors(ColorID),
    PRIMARY KEY (EpisodeID, ColorID)
);

-- Creating the EpisodeSubjectMatter Junction Table
CREATE TABLE IF NOT EXISTS EpisodeSubjectMatter (
    EpisodeID VARCHAR(10),
    SubjectID INT,
    FOREIGN KEY (EpisodeID) REFERENCES Episodes(EpisodeID),
    FOREIGN KEY (SubjectID) REFERENCES SubjectMatter(SubjectID),
    PRIMARY KEY (EpisodeID, SubjectID)
);