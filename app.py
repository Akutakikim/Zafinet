from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (important for frontend integration)

# Database Connection
db = mysql.connector.connect(
    host="your-database-host",
    user="your-database-username",
    password="your-database-password",
    database="social_media_app"
)

# Helper function for database queries
def execute_query(query, params=None, fetchone=False):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        if fetchone:
            return cursor.fetchone()
        else:
            return cursor.fetchall()
    except Exception as e:
        print(f"Database Error: {e}")
        return None

# User Registration
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']
    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    try:
        execute_query(query, (username, email, password))
        db.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    user = execute_query(query, (email, password), fetchone=True)
    if user:
        return jsonify({"message": "Login successful!", "user": user}), 200
    else:
        return jsonify({"error": "Invalid credentials!"}), 401

# Create a Post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    user_id = data['user_id']
    content = data['content']
    query = "INSERT INTO posts (user_id, content) VALUES (%s, %s)"
    try:
        execute_query(query, (user_id, content))
        db.commit()
        return jsonify({"message": "Post created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fetch All Posts
@app.route('/posts', methods=['GET'])
def get_posts():
    query = "SELECT p.id, p.content, p.created_at, u.username FROM posts p JOIN users u ON p.user_id = u.id ORDER BY p.created_at DESC"
    posts = execute_query(query)
    return jsonify(posts), 200

# Send a Message
@app.route('/messages', methods=['POST'])
def send_message():
    data = request.json
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    message = data['message']
    query = "INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)"
    try:
        execute_query(query, (sender_id, receiver_id, message))
        db.commit()
        return jsonify({"message": "Message sent successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fetch Messages Between Two Users
@app.route('/messages/<int:sender_id>/<int:receiver_id>', methods=['GET'])
def get_messages(sender_id, receiver_id):
    query = "SELECT * FROM messages WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s) ORDER BY sent_at ASC"
    messages = execute_query(query, (sender_id, receiver_id, receiver_id, sender_id))
    return jsonify(messages), 200

# Premium Subscription
@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    user_id = data['user_id']
    payment_method = data['payment_method']
    query = "INSERT INTO subscriptions (user_id, payment_method) VALUES (%s, %s)"
    try:
        execute_query(query, (user_id, payment_method))
        db.commit()
        return jsonify({"message": "Subscription successful!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)