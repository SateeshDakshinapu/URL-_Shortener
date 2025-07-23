from flask import Flask, request, redirect, jsonify, render_template
from pymongo import MongoClient
import time
from app.utils import validate_url, generate_short_code  # ⬅️ Imported here

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb+srv://tiger:tigersateesh@cluster0.0ggj59e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['url_shortener']
url_collection = db['urls']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'Missing URL'}), 400

    if not validate_url(original_url):
        return jsonify({'error': 'Invalid URL format'}), 400

    short_code = generate_short_code()
    timestamp = int(time.time())

    url_collection.insert_one({
        'short_code': short_code,
        'original_url': original_url,
        'created_at': timestamp,
        'clicks': 0,
        'access_timestamps': []
    })

    return jsonify({'short_url': f'/r/{short_code}'}), 201

@app.route('/r/<short_code>')
def redirect_url(short_code):
    record = url_collection.find_one({'short_code': short_code})
    if not record:
        return jsonify({'error': 'Short code not found'}), 404

    url_collection.update_one(
        {'short_code': short_code},
        {'$inc': {'clicks': 1}, '$push': {'access_timestamps': int(time.time())}}
    )

    return redirect(record['original_url'])

@app.route('/analytics/<short_code>')
def get_analytics(short_code):
    record = url_collection.find_one({'short_code': short_code})
    if not record:
        return jsonify({'error': 'Short code not found'}), 404

    return jsonify({
        'original_url': record['original_url'],
        'clicks': record['clicks'],
        'created_at': record['created_at'],
        'access_timestamps': record.get('access_timestamps', [])
    })

# ✅ This route serves the HTML page that loads analytics visually
@app.route('/analytics_page/<short_code>')
def analytics_page(short_code):
    return render_template('analytics.html', short_code=short_code)

if __name__ == '__main__':
    app.run(debug=True)
