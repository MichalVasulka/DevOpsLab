from flask import Flask, render_template, request, jsonify
import requests
import os
import logging

app = Flask(__name__)

port = 8080
BACKEND_PORT = 5100

# vars
logging_dir = 'logs'

if not os.path.exists(logging_dir):
    os.makedirs(logging_dir)

logging.basicConfig(
    filename=os.path.join(logging_dir, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)





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
    try:
        response = requests.post(f'{BACKEND_URL}/posts', json={"title": title, "content": content})
        if response.status_code == 201:
            logging.info('Post created successfully')
            return jsonify({"message": "Post created successfully"}), 201
        else:
            logging.error('Failed to create post')
            return jsonify({"error": "Failed to create post"}), 500
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/posts')
def posts():
    # Send GET request to the backend API
    try:
        response = requests.get(BACKEND_URL + '/posts')
        if response.status_code == 200:
            posts = [{'id': post[0], 'title': post[1], 'content': post[2]} for post in response.json()['posts']]
            return render_template('posts.html', posts=posts)
        else:
            logging.error('Failed to fetch posts')
            return jsonify({"error": "Failed to fetch posts"}), 500
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)
