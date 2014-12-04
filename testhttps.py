import BaseHTTPServer, SimpleHTTPServer
import ssl
"""
Create pem with the following
openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
"""
class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("Hit GET request")
        self.send_response(200)
        self.end_headers()
        response = "<html><body><p>This is the body</p></body></html>"
        self.wfile.write(response)
        #self.wfile.close()

    def log_message(self, format, *args):
        return


httpd = BaseHTTPServer.HTTPServer(('localhost', 8443), MyRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='cert/server.pem', server_side=True)
httpd.serve_forever()
