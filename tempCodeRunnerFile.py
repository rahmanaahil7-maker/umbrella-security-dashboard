from flask import Flask, render_template, request, jsonify
import time

# Import all integrated engines
from hash_engine import generate_sha256_hash
from dictionary_attack import run_dictionary_attack
from brute_force import run_brute_force
from password_analyzer import analyze_password
from ai_analyzer import run_ai_analysis

app = Flask(__name__)

WEB_WORDLIST = ["123456", "password", "admin", "qwerty", "letmein", "secret123", "dragon", "monkey"]
WEB_CHARSET = "abc123"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    password = data.get('password', '')
    if not password: return jsonify({'error': 'No password provided'}), 400
        
    analysis = analyze_password(password)
    analysis['hash'] = generate_sha256_hash(password)
    
    recs = []
    if analysis['length'] < 8: recs.append("Increase length to at least 8 characters.")
    if not analysis['has_symbol']: recs.append("Include special characters.")
    if not analysis['has_upper'] or not analysis['has_lower']: recs.append("Use a mix of uppercase and lowercase letters.")
    if not analysis.get('has_digit'): recs.append("Add numeric digits.")
    if analysis['patterns_found']: recs.append("Avoid common dictionary words.")
    if not recs: recs.append("Strong structure detected!")
    
    analysis['recommendations'] = recs
    return jsonify(analysis)

@app.route('/api/attack', methods=['POST'])
def attack():
    data = request.json
    target_hash = data.get('hash', '')
    if not target_hash: return jsonify({'error': 'No hash provided'}), 400
        
    results = {}
    
    start_time = time.time()
    dict_match = run_dictionary_attack(target_hash, WEB_WORDLIST)
    dict_time = time.time() - start_time
    
    results['dictionary'] = {
        'found': bool(dict_match), 'password': dict_match,
        'attempts': len(WEB_WORDLIST), 'time': round(dict_time, 5)
    }
    
    start_time = time.time()
    bf_match, bf_attempts = run_brute_force(target_hash, WEB_CHARSET, max_length=3)
    bf_time = time.time() - start_time
    
    results['bruteforce'] = {
        'found': bool(bf_match), 'password': bf_match,
        'attempts': bf_attempts, 'time': round(bf_time, 5)
    }
    
    return jsonify(results)

@app.route('/api/ai_analyze', methods=['POST'])
def ai_analyze():
    data = request.json
    password = data.get('password', '')
    if not password: return jsonify({'error': 'No password provided'}), 400
    
    result = run_ai_analysis(password)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)