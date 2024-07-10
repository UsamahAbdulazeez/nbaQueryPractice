# NBA Data Query Playground

This project is a web application designed to help users practice and learn SQL by querying NBA data stored in a SQLite database. The data is retrieved from the [balldontlie API](https://www.balldontlie.io/) and includes information on teams, players, games, and player stats. The project also aims to provide experience with pulling data from APIs.

## Purpose and Objectives

The main objectives of this project are:

- **SQL Practice**: Provide an interactive platform where users can practice and learn SQL.
- **Data Retrieval**: Gain experience in pulling data from APIs and managing it in a database.
- **User Interaction**: Create a user-friendly web interface for querying data.
- **Natural Language Processing**: Enable users to convert natural language queries into SQL.

## Features

- Fetch and store NBA data (teams, players, games, stats) from the balldontlie API.
- Store the data in a SQLite database.
- Web interface to query the data using SQL.
- Natural language to SQL query suggestions using OpenAI.

## Technologies Used

- Python
- Flask
- SQLite
- Pandas
- Requests
- OpenAI
- HTML/CSS

## Setup and Installation

### Prerequisites

- Python 3.x
- Flask
- Pandas
- Requests
- OpenAI Python package
- SQLite

### Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/nba-data-query-playground.git
    cd nba-data-query-playground
    ```

2. **Create a virtual environment and activate it**:

    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3. **Install the dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up API keys**:

    Replace the placeholders in the `fetch_data.py` and `app.py` files with your actual API keys.

    ```python
    # fetch_data.py and app.py
    API_KEY = 'your-balldontlie-api-key'
    OPENAI_API_KEY = 'your-openai-api-key'
    ```

### Usage

1. **Retrieve NBA Data**:

    Run the script to fetch data from the balldontlie API and store it in CSV files and SQLite database:

    ```sh
    python fetch_data.py
    ```

2. **Run the Flask Application**:

    ```sh
    python app.py
    ```

3. **Open your web browser** and go to `http://127.0.0.1:5000/` to use the application.

### Project Structure

- `fetch_data.py`: Script to fetch data from the balldontlie API and store it in CSV files and SQLite database.
- `app.py`: Flask application to provide a web interface for querying the data.
- `templates/index.html`: HTML template for the web interface.
- `static/style.css`: CSS for the web interface.
- `requirements.txt`: List of Python dependencies.

### Example Queries

- **Find all players with the position 'G'**:

    ```sql
    SELECT * FROM players WHERE position = 'G';
    ```

- **List all teams in the East conference**:

    ```sql
    SELECT * FROM teams WHERE conference = 'East';
    ```

- **Get the names and weights of all players in team 1**:

    ```sql
    SELECT first_name, last_name, weight_pounds FROM players WHERE team_id = 1;
    ```
