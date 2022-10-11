CREATE TABLE player_avg_misconduct (
player_id INT NOT NULL UNIQUE,
player_name VARCHAR(255) NOT NULL,
player_position VARCHAR(255) NOT NULL,
player_age INT NULL,
player_avg_yellow_cards FLOAT NOT NULL,
player_avg_red_cards FLOAT NOT NULL,
player_avg_fouls FLOAT NOT NULL,
PRIMARY KEY (player_id)
);

CREATE TEMPORARY TABLE player_misconduct (
player_id INT NOT NULL UNIQUE,
player_name VARCHAR(255) NOT NULL,
player_position VARCHAR(255) NOT NULL,
player_age INT NULL,
sum_yellow_cards INT NOT NULL,
sum_red_cards INT NOT NULL,
sum_fouls INT NOT NULL,
seasons_played INT NOT NULL,
PRIMARY KEY (player_id)
);

CREATE TEMPORARY TABLE player_ages (
player_id INT NOT NULL UNIQUE,
player_age INT NULL DEFAULT -1,
PRIMARY KEY (player_id)
);

INSERT INTO player_ages 
SELECT player_id, FLOOR((CURDATE() - player_birthday) / 10000) -- determines the players age
FROM players;

INSERT INTO player_misconduct 
SELECT p.player_id, p.player_name, p.player_position, pa.player_age, SUM(ds.player_yellow_cards), SUM(ds.player_red_cards), SUM(ds.player_fouls), COUNT(ds.player_id)
FROM defender_statistics AS ds
JOIN players AS p
ON p.player_id = ds.player_id
JOIN player_ages AS pa
ON p.player_id = pa.player_id
WHERE ds.player_appearances > 0
GROUP BY p.player_id, p.player_name;

INSERT INTO player_misconduct 
SELECT p.player_id, p.player_name, p.player_position, pa.player_age, SUM(fs.player_yellow_cards), SUM(fs.player_red_cards), SUM(fs.player_fouls), COUNT(fs.player_id)
FROM forward_statistics AS fs
JOIN players AS p
ON p.player_id = fs.player_id
JOIN player_ages AS pa
ON p.player_id = pa.player_id
WHERE fs.player_appearances > 0
GROUP BY p.player_id, p.player_name;

INSERT INTO player_misconduct 
SELECT p.player_id, p.player_name, p.player_position, pa.player_age, SUM(ms.player_yellow_cards), SUM(ms.player_red_cards), SUM(ms.player_fouls), COUNT(ms.player_id)
FROM midfielder_statistics AS ms
JOIN players AS p
ON p.player_id = ms.player_id
JOIN player_ages AS pa
ON p.player_id = pa.player_id
WHERE ms.player_appearances > 0
GROUP BY p.player_id, p.player_name;

INSERT INTO player_misconduct 
SELECT p.player_id, p.player_name, p.player_position, pa.player_age, SUM(gs.player_yellow_cards), SUM(gs.player_red_cards), SUM(gs.player_fouls), COUNT(gs.player_id)
FROM goalie_statistics AS gs
JOIN players AS p
ON p.player_id = gs.player_id
JOIN player_ages AS pa
ON p.player_id = pa.player_id
WHERE gs.player_appearances > 0
GROUP BY p.player_id, p.player_name;

INSERT INTO player_avg_misconduct
SELECT player_id, player_name, player_position, player_age, (sum_yellow_cards / seasons_played), (sum_red_cards / seasons_played), (sum_fouls / seasons_played)
FROM player_misconduct;

SELECT * FROM player_avg_misconduct;

SELECT * FROM player_misconduct;


-- Just for fun -- 
SELECT player_id, player_name, player_season, player_primary_club, player_goals
FROM goalie_statistics
WHERE player_goals > 0;

