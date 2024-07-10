from flask import Flask, request, render_template, session
import sqlite3
from openai import OpenAI
import logging
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with your secret key for session management

# Hard-coded OpenAI API key for debugging purposes
api_key = 'your_api_key'

if not api_key:
    app.logger.error("OPENAI_API_KEY not found in environment variables")
else:
    app.logger.debug(f"Loaded OPENAI_API_KEY: {api_key}")

# Instantiate the OpenAI client
client = OpenAI(api_key=api_key)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

# SQLite setup
def get_db():
    return sqlite3.connect('playground.db')

# Define schema information for the tables
schema_info = {
    'players': {
        'columns': ['id', 'first_name', 'last_name', 'position', 'height_feet', 'weight_pounds', 'team_id'],
        'example_row': [1, 'John', 'Doe', 'G', 6, 180, 1]
    },
    'teams': {
        'columns': ['id', 'abbreviation', 'city', 'conference', 'division', 'full_name', 'name'],
        'example_row': [1, 'BOS', 'Boston', 'East', 'Atlantic', 'Boston Celtics', 'Celtics']
    },
    'games': {
        'columns': ['id', 'date', 'home_team_id', 'visitor_team_id', 'home_team_score', 'visitor_team_score'],
        'example_row': [1, '2023-09-09', 1, 2, 100, 90]
    },
    'stats': {
        'columns': ['id', 'player_id', 'game_id', 'min', 'pts', 'reb', 'ast'],
        'example_row': [1, 1, 1, '32:00', 20, 10, 5]
    }
}

@app.route('/')
def index():
    players = get_table_data('players', limit=2)
    teams = get_table_data('teams', limit=2)
    games = get_table_data('games', limit=2)
    stats = get_table_data('stats', limit=2)
    return render_template('index.html', players=players, teams=teams, games=games, stats=stats, result=None, query="", error=None, suggested_query=None)

@app.route('/query', methods=['POST'])
def query():
    query_text = request.form.get('query_text')
    natural_language = request.form.get('natural_language')
    result = None
    error = None
    suggested_query = None

    app.logger.debug(f"Received query: Text={query_text}")

    if 'context' not in session:
        session['context'] = ""

    if request.form.get('execute'):
        try:
            app.logger.debug("Executing SQL query")
            result = query_sql(query_text)
            app.logger.debug(f"Query result: {result}")
        except Exception as e:
            error = str(e)
            app.logger.error(f"Error executing query: {error}")
    elif request.form.get('suggest'):
        app.logger.debug("Generating query suggestion")
        suggested_query = get_llm_suggestion(natural_language)
        app.logger.debug(f"Suggested query: {suggested_query}")

    players = get_table_data('players', limit=2)
    teams = get_table_data('teams', limit=2)
    games = get_table_data('games', limit=2)
    stats = get_table_data('stats', limit=2)

    return render_template('index.html', players=players, teams=teams, games=games, stats=stats, result=result, query=query_text, error=error, suggested_query=suggested_query)

def get_table_data(table_name, limit=2):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
        app.logger.debug(f"Retrieved {len(rows)} rows from {table_name}")
        return {"columns": columns, "rows": rows}
    except Exception as e:
        app.logger.error(f"Error retrieving data from {table_name}: {str(e)}")
        raise

def query_sql(query_text):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query_text)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
        app.logger.debug(f"SQL query executed successfully. Columns: {columns}, Row count: {len(rows)}")
        return {"columns": columns, "rows": rows}
    except Exception as e:
        app.logger.error(f"Error in SQL query execution: {str(e)}")
        raise

def get_llm_suggestion(natural_language):
    try:
        # Example natural language queries and their corresponding SQL queries
        examples = """
        Natural language: "Find all players with the position 'G'."
        SQL query: SELECT * FROM players WHERE position = 'G';

        Natural language: "List all teams in the East conference."
        SQL query: SELECT * FROM teams WHERE conference = 'East';

        Natural language: "Get the names and weights of all players in team 1."
        SQL query: SELECT first_name, last_name, weight_pounds FROM players WHERE team_id = 1;

        Natural language: "Show all teams in the West conference."
        SQL query: SELECT * FROM teams WHERE conference = 'West';

        Natural language: "Find players with a height greater than 6 feet."
        SQL query: SELECT * FROM players WHERE height_feet > 6;

        Natural language: "Count the number of teams in each conference."
        SQL query: SELECT conference, COUNT(*) FROM teams GROUP BY conference;
        """

        # Include schema information in the prompt
        schema_str = "\n".join([f"Table {table}: Columns = {info['columns']}" for table, info in schema_info.items()])

        # Create the prompt with schema information, examples, and the user's natural language request
        prompt = f"Schema:\n{schema_str}\n\nExamples:\n{examples}\n\nUser: {natural_language}\nConvert the above request to a SQL query:\n"

        app.logger.debug(f"Generated prompt for OpenAI: {prompt}")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts natural language to SQL queries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.3,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        
        suggested_query = response.choices[0].message.content.strip()

        app.logger.debug(f"Generated suggestion: {suggested_query}")
        return suggested_query
    except Exception as e:
        app.logger.error(f"Error generating suggestion with OpenAI: {str(e)}")
        return "Error generating suggestion"

if __name__ == '__main__':
    app.run(debug=True)