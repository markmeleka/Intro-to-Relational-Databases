#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
# function names and docstrings provided
# functions written by me

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    QUERY = "DELETE FROM matches *;"
    cursor.execute(QUERY)

    #reset scores to 0
    QUERY = """
    UPDATE players 
    SET points = 0
    ;
    """
    cursor.execute(QUERY)

    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    QUERY = "DELETE FROM players *;"
    cursor.execute(QUERY)
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    QUERY = "SELECT COUNT(*) FROM players;"
    cursor.execute(QUERY)
    player_count = cursor.fetchone()[0]
    #conn.commit()
    conn.close()
    return player_count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    # avoid SQL injection attack by inserting values using %s and 2nd argument of execute
    QUERY = "INSERT INTO players (full_name, points) VALUES (%s, %s);"
    data = (name, 0)
    cursor.execute(QUERY, data) 
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    
    conn = connect()
    cursor = conn.cursor()
    
    # match wins are empty

    # use an explicit join instead of an implicit join?
    QUERY = """
    SELECT players.id, players.full_name, players.points, 
    count(matches.match_id) as matches
    FROM players left join matches
    on players.id = matches.winner or players.id = matches.loser
    GROUP BY players.id, players.points
    ORDER BY players.points DESC
    ;
    """
    cursor.execute(QUERY)
    
    results = cursor.fetchall()

    conn.commit()
    conn.close()

    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()

    # Add match results into matches table
    QUERY = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    data = (winner, loser)
    cursor.execute(QUERY, data)

    # Get current points value for winning player
    QUERY = """
    SELECT players.points 
    FROM players
    WHERE players.id = %s;
    """
    data = (winner,)
    cursor.execute(QUERY, data)
    current_score = cursor.fetchall()[0][0]

    # Add one to points value for winning player
    new_score = current_score + 1
    QUERY = """
    UPDATE players 
    SET points = %s
    WHERE players.id = %s
    ;
    """
    data = (new_score, winner)
    cursor.execute(QUERY, data)

    conn.commit()
    conn.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    players_ranked = playerStandings()
    pairings = []

    temp = []

    for player in players_ranked:
        for item in player[0:2]:
            temp.append(item)
        if len(temp) == 4:
            pairings.append(tuple(temp))
            temp = []
            
    return pairings

