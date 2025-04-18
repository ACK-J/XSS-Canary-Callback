# app.py
from flask import Flask, request, render_template, Response
from flask_cors import CORS
import json
import os
import functools
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Get password from environment variable
DASHBOARD_PASSWORD = os.getenv('DASHBOARD_PASSWORD')
if not DASHBOARD_PASSWORD:
    raise ValueError("DASHBOARD_PASSWORD environment variable must be set using the following command: export DASHBOARD_PASSWORD=$(openssl rand -base64 32) && echo $DASHBOARD_PASSWORD")

def require_auth(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != 'admin' or auth.password != DASHBOARD_PASSWORD:
            return Response(
                'Unauthorized', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated

def load_json_data():
    try:
        data = []
        with open('xss_canary.json', 'r') as file:
            for line in file:
                try:
                    data.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        return data
    except FileNotFoundError:
        return []

@app.route('/', methods=['GET'])
def index():
    return "It's working!"
    
@app.route('/xss', methods=['GET'])
def xss_index():
    return "It's working!"

@app.route('/xss', methods=['POST'])
def xss_canary():
    canary_data = request.get_json()
    required_fields = ['alert_msg', 'stack', 'url', 'ref', 'timestamp']
    
    if not canary_data or not all(key in canary_data for key in required_fields):
        return "Invalid data", 400

    # Ensure timestamp exists or add it
    if not canary_data.get('timestamp'):
        canary_data['timestamp'] = datetime.now().isoformat()

    with open('xss_canary.json', 'a') as log_file:
        json.dump(canary_data, log_file)
        log_file.write("\n")

    return '', 204

@app.route('/dashboard')
@require_auth
def dashboard():
    data = load_json_data()
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    print("=" * 50)
    print("Access the dashboard at http://localhost:9000/dashboard")
    print("Username: admin")
    print("Password: [Set in DASHBOARD_PASSWORD environment variable]")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=9000)
