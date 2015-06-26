import BaseHTTPServer, SimpleHTTPServer
import httplib
import ssl
import threading


#openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -days 2048
#Then cat key.pem >> cert.pem

def proxyrequest(host, method, port, path, headers, body):
    print(dict(headers))
    if (port == 80):
        conn = httplib.HTTPConnection(host)
        conn.request(method, path, headers=dict(headers))
    elif (port == 443):
        conn = httplib.HTTPSConnection(host)
        conn.request(method, path, body=body, headers=dict(headers) )
    else:
        return None
    data = conn.getresponse()
    #conn.close()
    #print(dir(data))
    return data

class StoppableHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """http request handler with QUIT stopping the server"""
    
    def do_GET(self):
        #This gets changed to server_version
        self.server_version = ""
        self.sys_version = ""
        tempport = self.server.server_address[1]
        print(self.client_address[0])
        temphost = self.headers.getheader("host")
        temppath = self.path
        response = proxyrequest(temphost, "GET", tempport, temppath, self.headers, None)
        self.send_response(response.status)
        for header in response.getheaders():
            self.send_header(header[0], header[1])
        print(self.headers)
        self.end_headers()
        self.wfile.write(response.read())
        response.close()

    def do_POST(self):
        #This is the same reason as the do_GET method
        self.server_version = ""
        self.sys_version = ""
        print(self.server.server_address[1])
        #print(self.headers)
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)
        print(self.headers)
        print(data)
        tempport = self.server.server_address[1]
        temphost = self.headers.getheader("host")
        temppath = self.path
        response = proxyrequest(temphost, "POST", tempport, temppath, self.headers, data)
        self.send_response(response.status)
        for header in response.getheaders():
            self.send_header(header[0], header[1])
        self.end_headers()
        self.wfile.write(response.read())
        response.close()       

    def do_QUIT (self):
        """send 200 OK response, and set server.stop to True"""    
        self.send_response(200)
        self.end_headers()
        if self.client_address[0] == "127.0.0.1":
            self.server.stop = True

class StoppableHTTPServer (BaseHTTPServer.HTTPServer):
    """http server that reacts to self.stop flag"""

    def serve_forever (self):
        """Handle one request at a time until stopped."""
        self.stop = False
        print(self.server_address)
        while not self.stop:
            self.handle_request()

httpsd = StoppableHTTPServer(('0.0.0.0', 443), StoppableHTTPRequestHandler)
httpsd.socket = ssl.wrap_socket (httpsd.socket, certfile='./lib/cert/cert.pem', server_side=True)
httpd = StoppableHTTPServer(('0.0.0.0', 80), StoppableHTTPRequestHandler)

if __name__ == "__main__":
    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()
    thread2 = threading.Thread(target=httpsd.serve_forever)
    thread2.start()
    print("WebserverRunning...")
    while True:
        gotexit = raw_input("type exit to quit")
        if gotexit == "exit":
            conn = httplib.HTTPSConnection("127.0.0.1")
            conn.request("QUIT", "/")
            data = conn.getresponse()
            conn = httplib.HTTPConnection("127.0.0.1")
            conn.request("QUIT", "/")
            data = conn.getresponse()
            break
