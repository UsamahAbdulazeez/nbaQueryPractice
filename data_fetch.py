import requests
import csv
import sqlite3
import pandas as pd
import time

# Hardcoded API key
API_KEY = 'c97478ef-95ce-43fc-88d9-4631282b8135'
headers = {'Authorization': API_KEY}

# Set delay between requests (in seconds)
REQUEST_DELAY = 1  # Adjust as needed based on API's rate limit
MAX_RECORDS = 500  # Maximum number of records to retrieve

def get_teams():
    """
    Fetches the list of NBA teams from the API and saves it to a CSV file.
    """
    url = 'https://api.balldontlie.io/v1/teams'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        teams = data.get('data', [])
        
        with open('teams.csv', 'w', newline='') as csvfile:
            fieldnames = ['id', 'abbreviation', 'city', 'conference', 'division', 'full_name', 'name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for team in teams:
                writer.writerow(team)
        print("Teams data saved to teams.csv")
        
        for team in teams:
            print(f"Team: {team['full_name']} ({team['abbreviation']}) - Conference: {team['conference']}, Division: {team['division']}")
    else:
        print(f"Failed to retrieve data: {response.status_code}")

def get_players():
    """
    Fetches the list of NBA players from the API and saves it to a CSV file.
    Handles pagination to ensure all players are retrieved.
    """
    url = 'https://api.balldontlie.io/v1/players'
    params = {'per_page': 100, 'page': 1}
    all_players = []

    while len(all_players) < MAX_RECORDS:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            players = data.get('data', [])
            if not players:
                break
            all_players.extend(players)
            params['page'] += 1
            time.sleep(REQUEST_DELAY)  # Add delay between requests
            if len(all_players) >= MAX_RECORDS:
                all_players = all_players[:MAX_RECORDS]  # Limit to MAX_RECORDS
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            break

    with open('players.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'first_name', 'last_name', 'position', 'height_feet', 'weight_pounds', 'team_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for player in all_players:
            player_data = {k: player.get(k, '') for k in fieldnames if k != 'team_id'}
            player_data['team_id'] = player['team']['id']
            writer.writerow(player_data)
    print("Players data saved to players.csv")

def get_games():
    """
    Fetches the list of NBA games from the API and saves it to a CSV file.
    """
    url = 'https://api.balldontlie.io/v1/games'
    params = {
        'per_page': 100,  # Retrieve more games per request
        'start_date': '2023-09-09', 
        'end_date': '2024-04-02',  # Example dates
        'page': 1
    }
    all_games = []

    while len(all_games) < MAX_RECORDS:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            games = data.get('data', [])
            if not games:
                break
            all_games.extend(games)
            params['page'] += 1
            time.sleep(REQUEST_DELAY)  # Add delay between requests
            if len(all_games) >= MAX_RECORDS:
                all_games = all_games[:MAX_RECORDS]  # Limit to MAX_RECORDS
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            break

    with open('games.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'date', 'home_team_id', 'visitor_team_id', 'home_team_score', 'visitor_team_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for game in all_games:
            game_data = {
                'id': game['id'],
                'date': game['date'],
                'home_team_id': game['home_team']['id'],
                'visitor_team_id': game['visitor_team']['id'],
                'home_team_score': game['home_team_score'],
                'visitor_team_score': game['visitor_team_score']
            }
            writer.writerow(game_data)
    print("Games data saved to games.csv")

    # Print sample of games (first 10)
    for game in all_games[:10]:
        print(f"Game ID: {game['id']} - Date: {game['date']} - Home Team: {game['home_team']['full_name']} vs Visitor Team: {game['visitor_team']['full_name']} - Score: {game['home_team_score']}:{game['visitor_team_score']}")

def get_stats():
    """
    Fetches the list of NBA player stats from the API and saves it to a CSV file.
    """
    url = 'https://api.balldontlie.io/v1/stats'
    params = {
        'per_page': 100,  # Retrieve more stats per request
        'start_date': '2023-09-09', 
        'end_date': '2024-04-02',  # Example dates
        'page': 1
    }
    all_stats = []

    while len(all_stats) < MAX_RECORDS:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            stats = data.get('data', [])
            if not stats:
                break
            all_stats.extend(stats)
            params['page'] += 1
            time.sleep(REQUEST_DELAY)  # Add delay between requests
            if len(all_stats) >= MAX_RECORDS:
                all_stats = all_stats[:MAX_RECORDS]  # Limit to MAX_RECORDS
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            break

    with open('stats.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'player_id', 'game_id', 'min', 'pts', 'reb', 'ast']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for stat in all_stats:
            stat_data = {
                'id': stat['id'],
                'player_id': stat['player']['id'],
                'game_id': stat['game']['id'],
                'min': stat.get('min', 'N/A'),
                'pts': stat.get('pts', 'N/A'),
                'reb': stat.get('reb', 'N/A'),
                'ast': stat.get('ast', 'N/A')
            }
            writer.writerow(stat_data)
    print("Stats data saved to stats.csv")

    # Print sample of stats (first 10)
    for stat in all_stats[:10]:
        print(f"Player ID: {stat['player']['id']} - Game ID: {stat['game']['id']} - Minutes: {stat.get('min', 'N/A')} - Points: {stat.get('pts', 'N/A')} - Rebounds: {stat.get('reb', 'N/A')} - Assists: {stat.get('ast', 'N/A')}")

def setup_database():
    """
    Sets up the SQLite database and loads data from CSV files into respective tables.
    """
    conn = sqlite3.connect('playground.db')
    cursor = conn.cursor()

    # Create players table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            position TEXT,
            height_feet INTEGER,
            weight_pounds INTEGER,
            team_id INTEGER
        )
    ''')

    # Create teams table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            abbreviation TEXT,
            city TEXT,
            conference TEXT,
            division TEXT,
            full_name TEXT,
            name TEXT
        )
    ''')

    # Create games table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            date TEXT,
            home_team_id INTEGER,
            visitor_team_id INTEGER,
            home_team_score INTEGER,
            visitor_team_score INTEGER
        )
    ''')

    # Create stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY,
            player_id INTEGER,
            game_id INTEGER,
            min TEXT,
            pts INTEGER,
            reb INTEGER,
            ast INTEGER
        )
    ''')

    # Load data from CSV files into the tables
    try:
        players_df = pd.read_csv('players.csv')
        teams_df = pd.read_csv('teams.csv')
        games_df = pd.read_csv('games.csv')
        stats_df = pd.read_csv('stats.csv')

        players_df.to_sql('players', conn, if_exists='replace', index=False)
        teams_df.to_sql('teams', conn, if_exists='replace', index=False)
        games_df.to_sql('games', conn, if_exists='replace', index=False)
        stats_df.to_sql('stats', conn, if_exists='replace', index=False)

        conn.commit()
    except Exception as e:
        print(f"Error loading data into database: {str(e)}")
    finally:
        conn.close()

    print("Database setup complete.")

if __name__ == "__main__":
    print("Retrieving Teams...")
    get_teams()
    print("\nRetrieving Players...")
    get_players()
    print("\nRetrieving Games...")
    get_games()
    print("\nRetrieving Stats...")
    get_stats()
    print("\nSetting up Database...")
    setup_database()
