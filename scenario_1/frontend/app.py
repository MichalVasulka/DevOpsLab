from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

port=8080
BACKEND_PORT=5100


# Environment of the application
ENV = os.getenv('ENV', 'dev')

# URL of the backend API
if ENV == 'prod':
    # when started as container, contact VM host, not container localhost 
    # docker run -it -e ENV=prod -p 8080:8080 your-docker-image
    BACKEND_URL = f'http://host.docker.internal:{BACKEND_PORT}'
else:
    BACKEND_URL = f'http://localhost:{BACKEND_PORT}'


# --- API endpoints --- #

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
    response = requests.post(f'{BACKEND_URL}/posts', json={"title": title, "content": content})
    
    if response.status_code == 201:
        return jsonify({"message": "Post created successfully"}), 201
    else:
        return jsonify({"error": "Failed to create post"}), 500


@app.route('/posts')
def posts():
    # Send GET request to the backend API
    response = requests.get(BACKEND_URL + '/posts')

    if response.status_code == 200:
        # Convert the list of lists into a list of dictionaries
        posts = [{'id': post[0], 'title': post[1], 'content': post[2]} for post in response.json()['posts']]

        # Render a new template with the posts
        return render_template('posts.html', posts=posts)
    else:
        return jsonify({"error": "Failed to fetch posts"}), 500







if __name__ == '__main__':
    app.run(debug=True, port=port)
