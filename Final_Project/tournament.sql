-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- make sure your tables are normalized
-- don't forget PRIMARY KEYs and referenced keys
-- don't forget Bobby Tables (SQL Injection Attack) <- this is for python code

--Create DB. Do I need this in this file?
#CREATE DATABASE tournament;

-- connect to tournament DB
\c tournament;

-- I'll be importing this file multiple times as I'm debugging.
-- Will need to drop old tables to avoid errors. 
DROP TABLE IF EXISTS players, matches, match_results, points CASCADE; --list rest of tables here

CREATE TABLE players (id serial PRIMARY KEY, 
	full_name text,
	points integer); 

CREATE TABLE matches (match_id serial PRIMARY KEY, 
	--round_number varchar,
	winner serial REFERENCES players (id), 
	loser serial REFERENCES players (id)
	);

CREATE TABLE match_results (match_id serial REFERENCES matches (match_id), 
	round_number varchar,
	winner serial REFERENCES players (id), 
	loser serial REFERENCES players (id), 
	PRIMARY KEY (match_id, round_number)
	);

CREATE TABLE points (player_id serial REFERENCES players (id), 
	total_points integer
	);