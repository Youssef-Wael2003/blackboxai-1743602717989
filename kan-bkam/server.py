from flask import Flask, jsonify, send_from_directory, request
import json
import os

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/results')
def results():
    return app.send_static_file('results.html')

@app.route('/about.html')
def about():
    return app.send_static_file('about.html')

@app.route('/contact.html')
def contact():
    return app.send_static_file('contact.html')

@app.route('/data/products.json')
def serve_products():
    try:
        return send_from_directory('data', 'products.json', mimetype='application/json')
    except FileNotFoundError:
        return jsonify({'error': 'Products data not found'}), 404

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        # First try to load from API endpoint
        response = serve_products()
        if response.status_code != 200:
            raise FileNotFoundError(response.get_json()['error'])
            
        products = json.loads(response.get_data())
        
        # Support search query parameter
        search_query = request.args.get('q')
        if search_query:
            search_query = search_query.lower()
            products = [p for p in products if search_query in p['name'].lower()]
            
        return jsonify(products)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
