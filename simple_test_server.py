#!/usr/bin/env python3

"""
Simple HTTP server to test connectivity
"""

import os
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        message = f"""
        <html>
        <head><title>QuickDB Test Server</title></head>
        <body>
            <h1>QuickDB Test Server is Working!</h1>
            <p>This is a simple test server to verify network connectivity.</p>
            <p>Path requested: {self.path}</p>
        </body>
        </html>
        """
        
        self.wfile.write(message.encode())

def run_server(port=8080):
    server_address = ('0.0.0.0', port)
    
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"Starting test server on port {port}")
    print(f"You can access it at:")
    print(f"  - http://localhost:{port}")
    print(f"  - http://127.0.0.1:{port}")
    print(f"  - http://{local_ip}:{port}")
    
    try:
        httpd = HTTPServer(server_address, SimpleHandler)
        print("Server is running... Press CTRL+C to stop")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    run_server(port)