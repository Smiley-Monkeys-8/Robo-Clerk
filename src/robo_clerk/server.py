import http.server
import json
import socketserver
import os
import random

from robo_clerk.decider import judge

PORT = 8003
JSON_FOLDER = "out_archive_2"

class RandomPoemHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/random":
            self.send_error(404, "Only /random is supported")
            return

        files = [f for f in os.listdir(JSON_FOLDER) if f.endswith(".json")]
        if not files:
            self.send_error(404, "No poems found")
            return

        random_file = random.choice(files)
        with open(os.path.join(JSON_FOLDER, random_file), "r") as f:
            content = json.load(f)
        decision, result = judge.handcrafted_decision(os.path.join(JSON_FOLDER, random_file))
        
        content = {**content, **result}
        content["decision"] = decision.value

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(content).encode("utf-8"))


def run_server():
    Handler = RandomPoemHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving on http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
