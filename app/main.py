from flask import Flask, request, redirect, jsonify
import threading
import string
import random
import time
from urllib.parse import urlparse

app = Flask(__name__)

# In-memory stores
url_store = {}
click_stats = {}
lock = threading.Lock()

# Helper function to generate short codes
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# Route to shorten a URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'Missing URL'}), 400

    parsed_url = urlparse(original_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        return jsonify({'error': 'Invalid URL format'}), 400

    short_code = generate_short_code()
    timestamp = int(time.time())

    with lock:
        url_store[short_code] = {
            'original_url': original_url,
            'created_at': timestamp,
            'clicks': 0
        }
        click_stats[short_code] = []

    return jsonify({'short_url': f'/r/{short_code}'}), 201

# Route to redirect
@app.route('/r/<short_code>', methods=['GET'])
def redirect_url(short_code):
    with lock:
        url_data = url_store.get(short_code)
        if not url_data:
            return jsonify({'error': 'Short code not found'}), 404
        url_data['clicks'] += 1
        click_stats[short_code].append(int(time.time()))
        return redirect(url_data['original_url'])

# Route to get analytics
@app.route('/analytics/<short_code>', methods=['GET'])
def get_analytics(short_code):
    with lock:
        if short_code not in url_store:
            return jsonify({'error': 'Short code not found'}), 404
        data = url_store[short_code]
        return jsonify({
            'original_url': data['original_url'],
            'clicks': data['clicks'],
            'created_at': data['created_at'],
            'access_timestamps': click_stats.get(short_code, [])
        })

