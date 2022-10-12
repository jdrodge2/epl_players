CREATE TEMPORARY TABLE player_misconduct (
player_id INT NOT NULL,
player_name VARCHAR(255) NOT NULL,
player_position VARCHAR(255) NOT NULL,
player_season VARCHAR(255) NOT NULL, 
player_age INT NULL,
player_yellow_cards INT NOT NULL,
player_red_cards INT NOT NULL,
player_fouls INT NOT NULL
);

INSERT INTO player_misconduct
SELECT p.player_id, p.player_name, p.player_position, fs.player_season, FLOOR((es.season_end - p.player_birthday) / 10000) AS player_age, fs.player_yellow_cards, fs.player_red_cards, fs.player_fouls
FROM forward_statistics AS fs
JOIN players AS p
ON fs.player_id = p.player_id
JOIN end_of_season AS es
ON fs.player_season = es.season
WHERE fs.player_appearances > 0;

INSERT INTO player_misconduct
SELECT p.player_id, p.player_name, p.player_position, ms.player_season, FLOOR((es.season_end - p.player_birthday) / 10000) AS player_age, ms.player_yellow_cards, ms.player_red_cards, ms.player_fouls
FROM midfielder_statistics AS ms
JOIN players AS p
ON ms.player_id = p.player_id
JOIN end_of_season AS es
ON ms.player_season = es.season
WHERE ms.player_appearances > 0;

INSERT INTO player_misconduct
SELECT p.player_id, p.player_name, p.player_position, ds.player_season, FLOOR((es.season_end - p.player_birthday) / 10000) AS player_age, ds.player_yellow_cards, ds.player_red_cards, ds.player_fouls
FROM defender_statistics AS ds
JOIN players AS p
ON ds.player_id = p.player_id
JOIN end_of_season AS es
ON ds.player_season = es.season
WHERE ds.player_appearances > 0;

INSERT INTO player_misconduct
SELECT p.player_id, p.player_name, p.player_position, gs.player_season, FLOOR((es.season_end - p.player_birthday) / 10000) AS player_age, gs.player_yellow_cards, gs.player_red_cards, gs.player_fouls
FROM goalie_statistics AS gs
JOIN players AS p
ON gs.player_id = p.player_id
JOIN end_of_season AS es
ON gs.player_season = es.season
WHERE gs.player_appearances > 0;

SELECT player_id, player_name, player_position, SUM(player_yellow_cards) AS sum_yellow_cards, SUM(player_red_cards) AS sum_red_cards, SUM(player_fouls) AS player_fouls, COUNT(player_id) AS seasons_played
FROM player_misconduct
GROUP BY player_id, player_name, player_position
ORDER BY player_id ASC;

-- Just for fun -- 
-- SELECT player_id, player_name, player_season, player_primary_club, player_goals
-- FROM goalie_statistics
-- WHERE player_goals > 0;


