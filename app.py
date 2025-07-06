from flask import Flask, request, render_template, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ----------------------------
# MongoDB Atlas connection
# ----------------------------
uri = "mongodb+srv://jassu78:9491011303@cluster0.75pcejp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Confirm connection
try:
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print("❌ Connection error:", e)

# Select database and collection
db = client['webhookdb']
events_collection = db['events']

# ----------------------------
# Routes
# ----------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json

    # Determine GitHub event type from headers
    event_type = request.headers.get('X-GitHub-Event')
    event = {}

    if event_type == 'push':
        event = {
            'type': 'push',
            'author': data['pusher']['name'],
            'to_branch': data['ref'].split('/')[-1],
            'timestamp': datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
        }
    elif event_type == 'pull_request':
        action = data['action']
        if action in ['opened', 'closed']:
            event = {
                'type': 'pull_request',
                'author': data['pull_request']['user']['login'],
                'from_branch': data['pull_request']['head']['ref'],
                'to_branch': data['pull_request']['base']['ref'],
                'timestamp': datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
            }
    else:
        # Ignore other events
        return jsonify({'status': 'ignored'}), 200

    # Insert event into MongoDB
    events_collection.insert_one(event)
    return jsonify({'status': 'success'}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(events_collection.find({}, {'_id': 0}))
    return jsonify(events)

# ----------------------------
# Main entry point
# ----------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
