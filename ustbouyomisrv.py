# -*- coding:utf-8 -*-

import pprint
import urllib
import urlparse
import subprocess
import BaseHTTPServer
import SimpleHTTPServer


HTTP_PORT = 50000

REMOTE_TALK = [r'C:\path\to\RemoteTalk.exe', r'/T']


class BouyomiHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)

        try:
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
        except:
            params = {}

        if "t" in params:
            msg = params["t"]
            if msg != "":
                msg = urllib.unquote(msg).decode('utf-8')
                cmd = list(REMOTE_TALK)
                cmd.append(msg.encode('shift-jis'))
                try:
                    subprocess.call(cmd)
                except:
                    pass

        body = b'{}'
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)


def start_server():
    server_address = ("", HTTP_PORT)
    server = BaseHTTPServer.HTTPServer(server_address, BouyomiHandler)
    server.serve_forever()


if __name__ == "__main__":
    start_server()
