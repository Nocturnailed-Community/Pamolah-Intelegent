import mysql.connector
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Konfigurasi Database
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'deep_dental'
}

# Konfigurasi JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

# Fungsi untuk Membuat Koneksi ke Database
def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Endpoint Home
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Deep Dental API!"})

# ====================== USERS ======================
# Registrasi User
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'patient')
    full_name = data.get('full_name')
    email = data.get('email')
    phone_number = data.get('phone_number', None)
    date_of_birth = data.get('date_of_birth', None)
    gender = data.get('gender', None)
    address = data.get('address', None)

    if not username or not password or not full_name or not email:
        return jsonify({"error": "Username, password, full_name, and email are required"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, password, role, full_name, email, phone_number, date_of_birth, gender, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (username, hashed_password, role, full_name, email, phone_number, date_of_birth, gender, address))
            conn.commit()
            return jsonify({"message": "User registered successfully"}), 201
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Unable to connect to database"}), 500

# Login User
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

        access_token = create_access_token(identity=user["id"])
        return jsonify({"access_token": access_token, "role": user["role"]}), 200
    else:
        return jsonify({"error": "Unable to connect to database"}), 500

# ====================== DIAGNOSIS ======================
# Buat Diagnosis Baru
@app.route('/diagnosis', methods=['POST'])
@jwt_required()
def create_diagnosis():
    data = request.json
    user_id = get_jwt_identity()
    image_path = data.get('image_path')
    complaint = data.get('complaint')
    diagnosis_result = data.get('diagnosis_result')

    if not image_path or not complaint or not diagnosis_result:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO diagnosis (user_id, image_path, complaint, diagnosis_result)
                VALUES (%s, %s, %s, %s)
            """, (user_id, image_path, complaint, diagnosis_result))
            conn.commit()
            return jsonify({"message": "Diagnosis created successfully"}), 201
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Unable to connect to database"}), 500

# Ambil Semua Diagnosis
@app.route('/diagnosis', methods=['GET'])
@jwt_required()
def get_diagnoses():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM diagnosis WHERE user_id = %s", (user_id,))
        diagnoses = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(diagnoses), 200
    else:
        return jsonify({"error": "Unable to connect to database"}), 500

# ====================== TREATMENT RECOMMENDATIONS ======================
# Buat Rekomendasi Perawatan
@app.route('/treatment-recommendations', methods=['POST'])
@jwt_required()
def create_treatment_recommendation():
    data = request.json
    diagnosis_id = data.get('diagnosis_id')
    recommendation = data.get('recommendation')

    if not diagnosis_id or not recommendation:
        return jsonify({"error": "Diagnosis ID and recommendation are required"}), 400

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO treatment_recommendations (diagnosis_id, recommendation)
                VALUES (%s, %s)
            """, (diagnosis_id, recommendation))
            conn.commit()
            return jsonify({"message": "Treatment recommendation created successfully"}), 201
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Unable to connect to database"}), 500

# ====================== HEALTH HISTORY ======================
# Tambahkan Riwayat Kesehatan
@app.route('/health-history', methods=['POST'])
@jwt_required()
def add_health_history():
    data = request.json
    user_id = get_jwt_identity()
    condition_description = data.get('condition_description')

    if not condition_description:
        return jsonify({"error": "Condition description is required"}), 400

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO health_history (user_id, condition_description)
                VALUES (%s, %s)
            """, (user_id, condition_description))
            conn.commit()
            return jsonify({"message": "Health history added successfully"}), 201
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Unable to connect to database"}), 500

# ====================== PUBLIC AWARENESS ARTICLES ======================
# Tambahkan Artikel Kesadaran
@app.route('/awareness-articles', methods=['POST'])
@jwt_required()
def add_awareness_article():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    author = data.get('author')

    if not title or not content or not author:
        return jsonify({"error": "Title, content, and author are required"}), 400

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO awareness_articles (title, content, author)
                VALUES (%s, %s, %s)
            """, (title, content, author))
            conn.commit()
            return jsonify({"message": "Article added successfully"}), 201
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Unable to connect to database"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)