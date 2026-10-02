import http.server, ssl, functools, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.'))
handler = functools.partial(http.server.SimpleHTTPRequestHandler)
srv = http.server.HTTPServer(('127.0.0.1', 8667), handler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('cert.pem', 'key.pem')
srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
srv.serve_forever()
