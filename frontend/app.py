from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# URL of the backend API
BACKEND_URL = 'http://localhost:5000/posts'

# Render the homepage with a form
@app.route('/')
def home():
    return render_template('index.html')

# Handle form submission and send POST request to backend
@app.route('/submit', methods=['POST'])
def submit():
    title = request.form['title']
    content = request.form['content']

    # Send POST request to the backend API
    response = requests.post(BACKEND_URL, json={"title": title, "content": content})
    
    if response.status_code == 201:
        return jsonify({"message": "Post created successfully"}), 201
    else:
        return jsonify({"error": "Failed to create post"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=80)
