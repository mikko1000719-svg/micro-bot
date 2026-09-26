# -*- coding: utf-8 -*-
import os
from flask import Flask
from threading import Thread

# Create Flask application
app = Flask(__name__)

@app.route('/')
def home():
    """Provide Render health check response homepage"""
    return "[OK] WeiGuo Bot 5.0 is running!", 200

def run():
    # Read Render automatically assigned PORT environment variable, default to 10000 if not present
    port = int(os.environ.get("PORT", 10000))
    # Bind to 0.0.0.0 to receive external network requests
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    """Start Flask server using independent thread to avoid blocking Discord bot"""
    t = Thread(target=run)
    t.daemon = True
    t.start()
