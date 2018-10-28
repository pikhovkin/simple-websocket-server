import ssl
from optparse import OptionParser
try:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError:
    from http.server import HTTPServer, SimpleHTTPRequestHandler


if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog [options]', version='%prog 1.0')
    parser.add_option('--host', default='localhost', type='string', action='store', dest='host',
                      help='hostname (localhost)')
    parser.add_option('--port', default=443, type='int', action='store', dest='port', help='port (443)')
    parser.add_option('--cert', default='./cert.pem', type='string', action='store', dest='cert',
                      help='cert (./cert.pem)')
    parser.add_option('--key', default='./key.pem', type='string', action='store', dest='key', help='key (./key.pem)')
    parser.add_option('--ver', default=ssl.PROTOCOL_TLSv1, type=int, action='store', dest='ver', help='ssl version')

    (options, args) = parser.parse_args()

    # openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
    httpd = HTTPServer((options.host, options.port), SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, ssl_version=options.ver,
                                   certfile=options.cert, keyfile=options.key)
    httpd.serve_forever()
