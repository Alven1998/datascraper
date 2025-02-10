from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-scraping', methods=['POST'])
def start_scraping():
    try:
        subprocess.Popen(["python", "newdoc.py"])  # Runs newdoc.py
        return jsonify({"message": "Scraping started successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/close-server', methods=['POST'])
def close_server():
    try:
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func:
            shutdown_func()
        return jsonify({"message": "Server is shutting down..."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
