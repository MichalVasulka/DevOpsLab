from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to create a connection to SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('data.db')
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite DB: {e}")
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
        print("Table created successfully")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")




# curl -X POST \
#   http://localhost:5000/posts \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "title": "Example Title",
#     "content": "This is an example content for the post."
# }'
# API endpoint to handle POST requests
@app.route('/posts', methods=['POST'])
def create_post():
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
        conn.close()
        return jsonify({"message": "Post created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
