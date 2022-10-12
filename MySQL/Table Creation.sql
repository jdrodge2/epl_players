DROP TABLE forward_statistics;
DROP TABLE midfielder_statistics;
DROP TABLE defender_statistics;
DROP TABLE goalie_statistics;
DROP TABLE players;
DROP TABLE end_of_season;


CREATE TABLE end_of_season (
season VARCHAR(255) NOT NULL,
season_end DATE NOT NULL UNIQUE,
PRIMARY KEY (season)
);

CREATE TABLE players (
player_id INT NOT NULL UNIQUE,
player_name VARCHAR(255) NOT NULL,
player_position VARCHAR(255) NOT NULL,
player_nationality VARCHAR(255) NOT NULL, 
player_birthday DATE NULL,
player_height_cm INT NULL,
player_weight_kg INT NUll,
PRIMARY KEY (player_id)
);

CREATE TABLE forward_statistics (
player_id INT NOT NULL,
player_name VARCHAR(255) NOT NULL,
player_season VARCHAR(255) NOT NULL,
player_primary_club VARCHAR(255) NOT NULL,
player_secondary_club VARCHAR(255) NOT NULL,
player_appearances INT NOT NULL,
player_wins INT NOT NULL,
player_losses INT NOT NULL,
player_goals INT NOT NULL,
player_yellow_cards INT NOT NULL,
player_red_cards INT NOT NULL,
player_fouls INT NOT NULL,
player_penalties_scored INT NOT NULL,
player_freekicks_scored INT NOT NULL,
player_shots INT NOT NULL,
player_shots_on_target INT NOT NULL,
player_shooting_accuracy_percentage INT NOT NULL,
player_assists INT NOT NULL,
player_passes_per_match FLOAT NOT NULL,
player_big_chances_missed INT NOT NULL,
player_big_chances_created INT NOT NULL,
player_tackles INT NOT NULL,
player_offsides INT NOT NULL,
FOREIGN KEY (player_id) REFERENCES players(player_id),
FOREIGN KEY (player_season) REFERENCES end_of_season(season)
);

CREATE TABLE midfielder_statistics (
player_id INT NOT NULL,
player_name VARCHAR(255) NOT NULL,
player_season VARCHAR(255) NOT NULL,
player_primary_club VARCHAR(255) NOT NULL,
player_secondary_club VARCHAR(255) NOT NULL,
player_appearances INT NOT NULL,
player_wins INT NOT NULL,
player_losses INT NOT NULL,
player_goals INT NOT NULL,
player_yellow_cards INT NOT NULL,
player_red_cards INT NOT NULL,
player_fouls INT NOT NULL,
player_penalties_scored INT NOT NULL,
player_freekicks_scored INT NOT NULL,
player_shots INT NOT NULL,
player_shots_on_target INT NOT NULL,
player_shooting_accuracy_percentage INT NOT NULL,
player_assists INT NOT NULL,
player_passes_per_match FLOAT NOT NULL,
player_big_chances_missed INT NOT NULL,
player_big_chances_created INT NOT NULL,
player_tackles INT NOT NULL,
player_tackle_success_percentage INT NOT NULL,
player_duels_won INT NOT NULL,
player_duels_lost INT NOT NULL,
player_successful_50_50 INT NOT NULL,
player_aerial_battles_won INT NOT NULL,
player_aerial_battles_lost INT NOT NULL,
player_offsides INT NOT NULL,
FOREIGN KEY (player_id) REFERENCES players(player_id),
FOREIGN KEY (player_season) REFERENCES end_of_season(season)
);

CREATE TABLE defender_statistics (
player_id INT NOT NULL,
player_name VARCHAR(255) NOT NULL,
player_season VARCHAR(255) NOT NULL,
player_primary_club VARCHAR(255) NOT NULL,
player_secondary_club VARCHAR(255) NOT NULL,
player_appearances INT NOT NULL,
player_wins INT NOT NULL,
player_losses INT NOT NULL,
player_goals INT NOT NULL,
player_yellow_cards INT NOT NULL,
player_red_cards INT NOT NULL,
player_fouls INT NOT NULL,
player_assists INT NOT NULL,
player_passes_per_match FLOAT NOT NULL,
player_big_chances_created INT NOT NULL,
player_own_goals INT NOT NULL,
player_goals_conceded INT NOT NULL,
player_tackles INT NOT NULL,
player_tackle_success_percentage INT NOT NULL,
player_duels_won INT NOT NULL,
player_duels_lost INT NOT NULL,
player_successful_50_50 INT NOT NULL,
player_aerial_battles_won INT NOT NULL,
player_aerial_battles_lost INT NOT NULL,
player_clean_sheets INT NOT NULL,
player_offsides INT NOT NULL,
FOREIGN KEY (player_id) REFERENCES players(player_id),
FOREIGN KEY (player_season) REFERENCES end_of_season(season)
);

CREATE TABLE goalie_statistics (
player_id INT NOT NULL,
player_name VARCHAR(255) NOT NULL,
player_season VARCHAR(255) NOT NULL,
player_primary_club VARCHAR(255) NOT NULL,
player_secondary_club VARCHAR(255) NOT NULL,
player_appearances INT NOT NULL,
player_wins INT NOT NULL,
player_losses INT NOT NULL,
player_goals INT NOT NULL,
player_yellow_cards INT NOT NULL,
player_red_cards INT NOT NULL,
player_fouls INT NOT NULL,
player_assists INT NOT NULL,
player_passes_per_match FLOAT NOT NULL,
player_own_goals INT NOT NULL,
player_goals_conceded INT NOT NULL,
player_clean_sheets INT NOT NULL,
player_saves INT NOT NULL,
player_penalties_saved INT NOT NULL,
FOREIGN KEY (player_id) REFERENCES players(player_id),
FOREIGN KEY (player_season) REFERENCES end_of_season(season)
);

INSERT INTO end_of_season VALUES ('2021/2022', '2022-05-22');
INSERT INTO end_of_season VALUES ('2020/2021', '2021-05-23');
INSERT INTO end_of_season VALUES ('2019/2020', '2020-07-26');
INSERT INTO end_of_season VALUES ('2018/2019', '2019-05-12');

LOAD DATA LOCAL INFILE 'C:\\Users\\1rodg\\PycharmProjects\\epl-players\\venv\\CSV Files\\player_biographical.csv'
INTO TABLE players
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(player_id, player_name, player_position, player_nationality, @date_var, player_height_cm, player_weight_kg)
SET player_birthday = str_to_date(@date_var, '%Y-%m-%d');

LOAD DATA LOCAL INFILE 'C:\\Users\\1rodg\\PycharmProjects\\epl-players\\venv\\CSV Files\\attacker_stats.csv'
INTO TABLE forward_statistics
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:\\Users\\1rodg\\PycharmProjects\\epl-players\\venv\\CSV Files\\midfielder_stats.csv'
INTO TABLE midfielder_statistics
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:\\Users\\1rodg\\PycharmProjects\\epl-players\\venv\\CSV Files\\defender_stats.csv'
INTO TABLE defender_statistics
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:\\Users\\1rodg\\PycharmProjects\\epl-players\\venv\\CSV Files\\goalie_stats.csv'
INTO TABLE goalie_statistics
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

ALTER TABLE forward_statistics
ADD entry_id INT PRIMARY KEY UNIQUE AUTO_INCREMENT;

ALTER TABLE midfielder_statistics
ADD entry_id INT PRIMARY KEY UNIQUE AUTO_INCREMENT;

ALTER TABLE defender_statistics
ADD entry_id INT PRIMARY KEY UNIQUE AUTO_INCREMENT;

ALTER TABLE goalie_statistics
ADD entry_id INT PRIMARY KEY UNIQUE AUTO_INCREMENT;
