from flask import Flask, request, render_template, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# ----------------------------
# MongoDB Atlas connection
# ----------------------------

uri = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://jassu78:9491011303@cluster0.75pcejp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print("❌ Connection error:", e)

db = client['webhookdb']
events_collection = db['events']

# ----------------------------
# Routes
# ----------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['GET', 'POST', 'HEAD', 'OPTIONS'])
def github_webhook():
    if request.method == 'OPTIONS':
        return '', 200

    if request.method in ['GET', 'HEAD']:
        return "✅ Webhook endpoint is active.", 200

    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    event = {}

    # ----------------------------
    # Handle PUSH event
    # ----------------------------
    if event_type == 'push' and data and 'pusher' in data and 'ref' in data:
        head_commit = data.get('head_commit', {})
        timestamp = head_commit.get('timestamp', datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC"))
        event = {
            'type': 'push',
            'author': data['pusher']['name'],
            'to_branch': data['ref'].split('/')[-1],
            'timestamp': timestamp
        }

    # ----------------------------
    # Handle PULL REQUEST & MERGE events
    # ----------------------------
    elif event_type == 'pull_request' and data and 'pull_request' in data:
        action = data.get('action', '')
        pr = data['pull_request']
        if action == 'closed' and pr.get('merged', False):
            # MERGE event
            event = {
                'type': 'merge',
                'author': pr['user']['login'],
                'from_branch': pr['head']['ref'],
                'to_branch': pr['base']['ref'],
                'timestamp': pr['merged_at']
            }
        elif action == 'opened':
            # PULL REQUEST event
            event = {
                'type': 'pull_request',
                'author': pr['user']['login'],
                'from_branch': pr['head']['ref'],
                'to_branch': pr['base']['ref'],
                'timestamp': pr['created_at']
            }

    else:
        # Ignore other events
        return jsonify({'status': 'ignored'}), 200

    # ----------------------------
    # Insert into MongoDB
    # ----------------------------
    if event:
        events_collection.insert_one(event)
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'no_data'}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(events_collection.find({}, {'_id': 0}))
    return jsonify(events)

# ----------------------------
# Main entry point
# ----------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
