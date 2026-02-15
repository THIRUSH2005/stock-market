import http.server
import socketserver
import json
import random
import time
import os

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            time.sleep(1) # Simulated network latency
            
            user_message = data.get('message', '').lower()
            response_text = "I'm analyzing the market trends."
            
            if "apple" in user_message or "aapl" in user_message:
                response_text = "Apple (AAPL) is showing strong bullish momentum above the $189 resistance level. Options volume suggests a potential breakout."
            elif "tesla" in user_message or "tsla" in user_message:
                response_text = "Tesla (TSLA) is currently consolidating. The AI model predicts high volatility in the next 48 hours."
            elif "prediction" in user_message:
                response_text = "My predictive models indicate a general tech sector rally. I suggest looking at NVDA and AMD for short-term opportunities."
            
            response = {
                "status": "success",
                "message": response_text,
                "timestamp": time.time()
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
            
        # Fallback for other POST requests
        self.send_error(404, "File not found")
        return

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/portfolio':
            self.path = '/portfolio.html'
        elif self.path == '/analysis':
            self.path = '/analysis.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

print(f"Starting Server at http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
