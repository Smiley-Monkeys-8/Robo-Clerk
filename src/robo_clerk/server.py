import http.server
import socketserver
import json
import os
import random

from robo_clerk.decider import judge

PORT = 8000
JSON_FOLDER = "out"


class RandomPoemHandler(http.server.SimpleHTTPRequestHandler):
    def send_cors_headers(self):
        # Send CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        # Handle OPTIONS request (preflight)
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path != "/next-client":
            self.send_response(404)
            self.send_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Only /next-client is supported"}).encode())
            return

        files = [f for f in os.listdir(JSON_FOLDER) if f.endswith(".json")]
        if not files:
            self.send_response(404)
            self.send_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "No poems found"}).encode())
            return

        random_file = random.choice(files)
        with open(os.path.join(JSON_FOLDER, random_file), "r") as f:
            content = json.load(f)

        try:
            # If you're using the judge module
            decision, result = judge.handcrafted_decision(os.path.join(JSON_FOLDER, random_file))
            content = {**content, **result}
            content["decision"] = decision.value
        except:
            # If judge module is unavailable, provide a default decision
            if "decision" not in content:
                content["decision"] = "Accept" if random.random() > 0.3 else "Reject"

        self.send_response(200)
        self.send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(content).encode("utf-8"))


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def run_server():
    with ReusableTCPServer(("", PORT), RandomPoemHandler) as httpd:
        print(f"Serving on http://localhost:{PORT}")
        print(f"CORS headers enabled for all origins")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()