# webhook-repo

# webhook-repo

This repository contains a **Flask backend application** to receive GitHub webhooks for push, pull request, and merge events, store them in **MongoDB Atlas**, and display them on a clean frontend UI.

---

## 🚀 **Features**

✅ Receives **push**, **pull request**, and **merge** events via GitHub webhooks  
✅ Stores event data in **MongoDB Atlas**  
✅ Displays events on a **responsive HTML frontend**  
✅ Auto-refreshes every 15 seconds  
✅ Deployed on **Render**

---

## 🔗 **Live URL**

➡️ [https://webhook-repo-d3gz.onrender.com/](https://webhook-repo-d3gz.onrender.com/)

---

## ⚙️ **Setup Instructions**

### **1. Clone the repo**

```bash
git clone https://github.com/jassu78/webhook-repo.git
cd webhook-repo
2. Install dependencies
bash
Copy code
pip install -r requirements.txt
(Ensure requirements.txt includes Flask, pymongo, flask_cors, dnspython)

3. Set environment variables
Create a .env file or export directly:

bash
Copy code
export MONGO_URI="your MongoDB Atlas connection string"
4. Run the app locally
bash
Copy code
python app.py
App will be available at http://localhost:5000.

🔧 Endpoints
/
Renders frontend UI displaying all events.

/webhook [POST]
Receives GitHub webhook payloads for:

Push events

Pull request opened

Pull request merged (closed with merged: true)

✔️ Parses and stores events with author, branches, and timestamp.

/events [GET]
Returns all events as JSON for frontend polling.

📦 Deployment
This app is deployed on Render with:

Build Command: (leave blank for Python detection)

Start Command: python app.py

Environment Variables:

MONGO_URI: Your MongoDB connection string

🔗 GitHub Webhook Configuration
Configured in action-repo:

Payload URL: https://webhook-repo-d3gz.onrender.com/webhook

Content type: application/json

Events: Push, Pull Requests

🎨 Frontend UI
Displays events in the format:

Push: {author} pushed to {to_branch} on {timestamp}

Pull Request: {author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}

Merge: {author} merged branch {from_branch} to {to_branch} on {timestamp}

Updates automatically every 15 seconds.

👨‍💻 Author
Name: Jaswanth Jogi

Assessment: Developer Webhook Integration Task

📝 Notes
🔹 Ensure your MongoDB Atlas IP whitelist includes Render or 0.0.0.0/0.
🔹 Replace hardcoded MongoDB URI with environment variable for security in production.