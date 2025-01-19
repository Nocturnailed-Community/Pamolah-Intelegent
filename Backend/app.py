import mysql.connector
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)  # Enable CORS

# Konfigurasi Database
DB_CONFIG = {
    'host': '',
    'user': '',
    'password': '',
    'database': ''
}

# Konfigurasi JWT
app.config['JWT_SECRET_KEY'] = ''
jwt = JWTManager(app)

# Fungsi untuk Membuat Koneksi ke Database
def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Memuat model dan vectorizer
try:
    model = joblib.load('knn_model.pkl')
    tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
except FileNotFoundError:
    model = None
    tfidf_vectorizer = None
    print("Model atau vectorizer tidak ditemukan. Pastikan file 'knn_model.pkl' dan 'tfidf_vectorizer.pkl' tersedia.")

# Endpoint Home
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Microservice Sentiment Prediction!"})

# Registrasi User
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Hash password sebelum disimpan
    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"error": "Unable to connect to database"}), 500

# Login dan Mendapatkan JWT
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user or not check_password_hash(user['password'], password):
            return jsonify({"error": "Invalid username or password"}), 401

        # Generate JWT
        access_token = create_access_token(identity=user["username"])
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Unable to connect to database"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)