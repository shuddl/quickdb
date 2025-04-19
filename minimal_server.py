#!/usr/bin/env python3

"""
Minimal Flask server to test connectivity
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Server</title>
    </head>
    <body>
        <h1>It Works!</h1>
        <p>This is a minimal test server to verify network connectivity.</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("Starting minimal test server on 0.0.0.0:7000")
    print("Try accessing at:")
    print("- http://localhost:7000")
    print("- http://127.0.0.1:7000")
    
    # Run the app with very specific settings
    app.run(host='0.0.0.0', port=7000, debug=True, use_reloader=False)