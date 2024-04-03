from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import sqlite3
import os
import sys
import json
import Physics
import main
import urllib
import json

class MyHandler(BaseHTTPRequestHandler):
    playerNames = {}
    def do_GET(self):
        if self.path in ['/', '/frontPage.html']:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('frontPage.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/submit_shot':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        elif self.path == '/get_initial_table':
            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.end_headers()
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        if self.path == '/submit_player_names':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            playerName1 = data.get('playerName1')
            playerName2 = data.get('playerName2')
            self.playerNames['playerName1'] = playerName1
            self.playerNames['playerName2'] = playerName2

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'success'}
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path == '/get_svg_content':
           content_length = int(self.headers['Content-Length'])
           post_data = self.rfile.read(content_length)
           form_data = parse.parse_qs(post_data.decode('utf-8'))
           playerName1 = self.playerNames.get('playerName1', None)
           playerName2 = self.playerNames.get('playerName2', None)
           db = Physics.Database()

           firstTable = main.init_table()
           Physics.Game(gameName="Game01", player1Name = playerName1, player2Name = playerName2)
           svg_content = firstTable.svg()
           with open('index.html', 'r') as file:
               content = file.read().replace('${svg_content}', svg_content)
               content = content.replace('${playerName1}', playerName1)
               content = content.replace('${playerName2}', playerName2)
               self.send_response(200)
               self.send_header('Content-type', 'text/html')
               self.send_header("Content-length", str(len(content.encode('utf-8'))))
               self.end_headers()
               self.wfile.write(bytes(content, "utf-8"))
        elif self.path == '/submit_shot':
            self.handle_submit_shot()
        else:
            self.send_error(404, "Path not supported.")

    def read_post_data(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        return parse.parse_qs(post_data)

    def extract_position(self, data):
        x_position = float(data.get('dx', [0])[0])
        y_position = float(data.get('dy', [0])[0])
        return x_position, y_position

    def generate_frames_data(self, db, start_id, end_id):
        frames = []
        #loops through the table id's from start to end to generate frames 
        for i in range(start_id, end_id + 1):
            table = db.readTable(i)
            frames.append({
                "svg": table.svg().strip(),
                "time": table.time
            })
        return frames

    def handle_submit_shot(self):
        try:
            data = self.read_post_data()
            x_position, y_position = self.extract_position(data)

            db = Physics.Database()
            before_shot_id = db.getLastTableID() - 1
            game = Physics.Game(gameID=1)
            game.shoot("Game01", "Thanush", db.readTable(before_shot_id), x_position, y_position)
            after_shot_id = db.getLastTableID() - 1

            frames_data = {
                "frames": self.generate_frames_data(db, before_shot_id, after_shot_id)
            }

            self.respond_with_json(frames_data)
        except Exception as e:
            self.send_error(500, f"Server Error: {e}")

    def respond_with_json(self, data):
        json_response = json.dumps(data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', str(len(json_response)))
        self.end_headers()
        self.wfile.write(json_response.encode('utf-8'))
    

if __name__ == "__main__":
    port = 54091
    httpd = HTTPServer(('localhost', port), MyHandler)
    print("Server listening on port:", port)
    httpd.serve_forever()
