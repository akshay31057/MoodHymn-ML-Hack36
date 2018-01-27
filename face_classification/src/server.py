#!/usr/bin/env python3
 
import http.server
import http.server
import cgitb; cgitb.enable()  ## This line enables CGI error reporting
 
server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
server_address = ("localhost", 9998)
handler.cgi_directories = ["/"]
 
httpd = server(server_address, handler)
print('Server started')
httpd.serve_forever()

