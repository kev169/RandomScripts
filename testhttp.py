#!/usr/bin/env python3.4

from http.server   import HTTPServer, test
from http.server import SimpleHTTPRequestHandler
from socketserver     import ThreadingMixIn

from concurrent.futures import ThreadPoolExecutor # pip install futures

class PoolMixIn(ThreadingMixIn):
    def process_request(self, request, client_address):
        self.pool.submit(self.process_request_thread, request, client_address)

def main():
    class PoolHTTPServer(PoolMixIn, HTTPServer):
        pool = ThreadPoolExecutor(max_workers=40)

    test(HandlerClass=SimpleHTTPRequestHandler, ServerClass=PoolHTTPServer)

if __name__=="__main__":
    main()
