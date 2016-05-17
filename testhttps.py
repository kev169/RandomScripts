#import BaseHTTPServer, SimpleHTTPServer
import http.server as BaseHTTPServer
import http.server as SimpleHTTPServer
import ssl
import socketserver as SocketServer
from socketserver import ThreadingMixIn

from concurrent.futures import ThreadPoolExecutor
"""
Create pem with the following
openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
"""
class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        print("Hit GET request")
        self.send_response(200)
        self.end_headers()
        response = "<html><body><p>This is the body</p></body></html>".encode()
        self.wfile.write(response)
        #self.wfile.close()

    def log_message(self, format, *args):
        return

class PoolMixIn(ThreadingMixIn):
    def process_request(self, request, client_address):
        self.pool.submit(self.process_request_thread, request, client_address)

class ThreadingSimpleServer(PoolMixIn, BaseHTTPServer.HTTPServer):
    pool = ThreadPoolExecutor(max_workers=40)

#httpd = ThreadingSimpleServer(('localhost', 8443), MyRequestHandler)
httpd = BaseHTTPServer.HTTPServer(('localhost', 8443), MyRequestHandler)
#httpd.socket = ssl.wrap_socket (httpd.socket, certfile='cert/server.pem', server_side=True)
httpd.serve_forever()
