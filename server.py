from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import sqlite3
import os
import sys
import json
import Physics
import main
import urllib


class MyHandler(BaseHTTPRequestHandler):

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
        if self.path == '/get_svg_content':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = parse.parse_qs(post_data.decode('utf-8'))
            playerName1 = form_data.get('player1', [None])[0]
            playerName2 = form_data.get('player2', [None])[0]
            db = Physics.Database()
            firstTable = main.init_table()
            # Physics.Game(gameName='Game01', player1Name = playerName1, player2Name = playerName2)
            # game = Physics.Game(gameName="Game01", player1Name = playerName1, player2Name = playerName2)
            if not firstTable:
                self.send_error(500, 'Server Error: Table could not be initialized')
                return
            svg_content = firstTable.svg()

            with open('index.html', 'r') as file:
                content = file.read().replace('${svg_content}', svg_content)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header("Content-length", str(len(content.encode('utf-8'))))
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))
        elif self.path == '/submit_shot':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            dx = data.get('dx')
            dy = data.get('dy')

            db = Physics.Database()
            beforeShot = db.getLastTableID() - 1
            game = Physics.Game(gameID=1)
            afterShot = db.getLastTableID() - 1
            frameData = {
                "frames": []
            }
            i = beforeShot
            while (i <= afterShot):
                table = db.readTable(i)
                frameInfo = {
                    "svg": table.svg().strip(),
                    "time": table.time
                }
                frameData["frames"].append(frameInfo)
                i+=1

            print("Number of frames: ", len(frameData["frames"]))
            lastTable = db.readTable(afterShot)
            print(lastTable)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            jsonResponse = json.dumps(frameData)
            self.send_header('Content-Length', str(len(jsonResponse)))
            self.end_headers()
            self.wfile.write(jsonResponse.endcode('utf-8'))
    

if __name__ == "__main__":
    # main.init_table()
    port = 54091
    httpd = HTTPServer(('localhost', port), MyHandler)
    print("Server listening on port:", port)
    httpd.serve_forever()
