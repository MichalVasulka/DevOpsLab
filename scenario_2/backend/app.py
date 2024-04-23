# flask app with persistence and logging

from flask import Flask, request, jsonify
import sqlite3
import os
import logging

app = Flask(__name__)
port = 5100

# vars
logging_dir = 'logs'
data_dir = 'data'

if not os.path.exists(logging_dir):
    os.makedirs(logging_dir)

logging.basicConfig(
    filename=os.path.join(logging_dir, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# Function to create a connection to SQLite database
def create_connection():
    conn = None
    
    # Create 'data' directory if not exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    try:
        conn = sqlite3.connect(f'./{data_dir}/data.db')
        logging.info("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        logging.error(f"Error connecting to SQLite DB: {e}")
    return conn

# Function to create a table if it doesn't exist
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT
            )
        ''')
        logging.info("Table created successfully")
    except sqlite3.Error as e:
        logging.error(f"Error creating table: {e}")

# --- API Endpoints ---

@app.route('/health', methods=['GET'])
def health():
    # Return HTTP 200 OK status and a JSON payload
    return jsonify({'status': 'OK'}), 200

# API endpoint to handle GET requests
@app.route('/posts', methods=['GET'])
def get_posts():
    logging.info("Received GET request for /posts")
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Fetch all posts from the database
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()

        return jsonify({"posts": posts}), 200
    except Exception as e:
        logging.error(f"GET /posts failed: {e}")
        return jsonify({"error": str(e)}), 500

# API endpoint to handle POST requests
@app.route('/posts', methods=['POST'])
def create_post():
    logging.info("Received POST request for /posts")
    try:
        conn = create_connection()
        create_table(conn)
        cursor = conn.cursor()
        
        # Extract data from the request
        data = request.json
        title = data.get('title')
        content = data.get('content')

        # Insert data into the database
        cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        logging.info("Post created successfully")
        return jsonify({"message": "Post created successfully"}), 201
    except Exception as e:
        logging.error(f"POST /posts failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)
