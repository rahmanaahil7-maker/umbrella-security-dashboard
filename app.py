import os
import time
import math
from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from advanced_engines import generate_hash, parallel_brute_force
from ml_engine import ml_model
from report_engine import generate_pdf_report
from ai_analyzer import run_ai_analysis

app = Flask(__name__)
app.secret_key = 'enterprise_security_secret_token'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///benchmarks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='guest')  # Default role is now strictly 'guest'

class BenchmarkLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    algorithm = db.Column(db.String(20))
    time_elapsed = db.Column(db.Float)
    attempts = db.Column(db.Integer)
    hash_rate = db.Column(db.Float)
    cracked = db.Column(db.Boolean)
    executed_by = db.Column(db.String(50), default='Guest')
    timestamp = db.Column(db.Float, default=time.time)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        db.session.add(User(
            username='admin', 
            password_hash=generate_password_hash('admin123'),
            role='admin'
        ))
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

# --- Authentication Routes ---
@app.route('/api/auth/status')
def auth_status():
    if current_user.is_authenticated:
        return jsonify({"authenticated": True, "username": current_user.username, "role": current_user.role})
    return jsonify({"authenticated": False, "username": "Guest", "role": "guest"})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    user = User.query.filter_by(username=data.get('username')).first()
    if user and check_password_hash(user.password_hash, data.get('password', '')):
        login_user(user)
        return jsonify({"success": True, "username": user.username, "role": user.role})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if len(username) < 3 or len(password) < 6:
        return jsonify({"success": False, "message": "Username (min 3) or Password (min 6) too short."}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "message": "Username already taken."}), 400
    
    # Newly registered users are now forced into the 'guest' role
    new_user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role='guest' 
    )
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return jsonify({"success": True, "username": new_user.username, "role": new_user.role})

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"success": True})

# --- Engine Routes ---
@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    password = data.get('password', '')
    algorithm = data.get('algorithm', 'sha256')
    if not password: return jsonify({'error': 'Password is required'}), 400

    charset_pool = 0
    if any(c.islower() for c in password): charset_pool += 26
    if any(c.isupper() for c in password): charset_pool += 26
    if any(c.isdigit() for c in password): charset_pool += 10
    if any(not c.isalnum() for c in password): charset_pool += 33
    charset_pool = max(charset_pool, 1)

    entropy = round(len(password) * math.log2(charset_pool), 2)
    search_space = charset_pool ** len(password)
    hashed_str = generate_hash(password, algorithm)

    perplexity = ml_model.calculate_perplexity(password)
    risk_level = "High Vulnerability" if perplexity < 25 else "Moderate" if perplexity < 75 else "Low Vulnerability"
    
    curve_data = [{"length": l, "space": charset_pool ** l} for l in range(1, 11)]

    return jsonify({
        "length": len(password), "entropy": entropy, "search_space": f"{search_space:.2e}",
        "charset_pool": charset_pool, "hash": hashed_str, "algorithm": algorithm,
        "ml": {"perplexity": perplexity, "risk_level": risk_level, "predicted_next": ml_model.predict_next_chars(password, 3)},
        "curve": curve_data
    })

@app.route('/api/attack_parallel', methods=['POST'])
def attack_parallel():
    data = request.json or {}
    password = data.get('password', '')
    algorithm = data.get('algorithm', 'sha256')
    
    target_hash = generate_hash(password, algorithm)
    cracked_pw, time_elapsed, attempts = parallel_brute_force(
        target_hash=target_hash, charset=data.get('charset', 'abc123'), max_length=int(data.get('max_length', 3)), algorithm=algorithm, max_workers=4
    )

    hash_rate = round(attempts / time_elapsed, 1)
    username = current_user.username if current_user.is_authenticated else "Guest"

    log = BenchmarkLog(algorithm=algorithm, time_elapsed=time_elapsed, attempts=attempts, hash_rate=hash_rate, cracked=bool(cracked_pw), executed_by=username)
    db.session.add(log)
    db.session.commit()

    return jsonify({"cracked": bool(cracked_pw), "found_password": cracked_pw, "time": round(time_elapsed, 4), "attempts": attempts, "hash_rate": hash_rate, "algorithm": algorithm})

@app.route('/api/ai_analyze', methods=['POST'])
def ai_analyze_route():
    return jsonify(run_ai_analysis(request.json.get('password', '')))

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    data = request.json or {}
    try:
        pdf_path = generate_pdf_report(data.get('password', ''), run_ai_analysis(data.get('password', '')), data.get('bench_data', {}), data.get('ml_data', {}))
        return send_file(pdf_path, as_attachment=True, download_name="Security_Audit_Report.pdf", mimetype='application/pdf')
    except Exception as e:
        return jsonify({"error": f"PDF Generation Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)