import http.server
import ssl

from http.server import HTTPServer, BaseHTTPRequestHandler

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        ''' Present frontpage with user authentication. '''
        if self.headers['Authorization'] == None:
            self.do_AUTHHEAD()
            self.wfile.write(bytes('no auth header received', 'UTF-8'))
            pass
        elif self.headers['Authorization'] == 'Basic dXNlcm5hbWU6cGFzc3dvcmQ=':
            self.do_HEAD()
            #self.wfile.write(bytes(self.headers['Authorization'], 'UTF-8'))
            self.wfile.write(bytes('<H1>WELCOME, You\'re authenticated!</H1>', 'UTF-8'))
            pass
        else:
            self.do_AUTHHEAD()
            #self.wfile.write(bytes(self.headers['Authorization'], 'UTF-8'))
            self.wfile.write(bytes(' not authenticated, T-T', 'UTF-8'))
            pass

def main():
    try:
        server_address = ('localhost', 4443)
        httpd = http.server.HTTPServer(server_address, CustomHTTPRequestHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket,
                                       server_side=True,
                                       certfile="server.pem",
                                       ssl_version=ssl.PROTOCOL_TLS)
        sa = httpd.socket.getsockname()
        print ("Serving HTTP on", sa[0], "port", sa[1], "...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print ('^C received, shutting down server')
        httpd.socket.close()

if __name__ == '__main__':
    main()
