"""Extend Python's built in HTTP server to save files while still allowing gets

This webserver is BASIC. Do not hit it from multiple sophisticated browsers, and multiple machines.
It's meant for simple file get/put. It will likely timeout if under any significant load

curl or wget can be used to send files with options similar to the following

  curl -X PUT --upload-file somefile.txt http://localhost:8000
  wget -O- --method=PUT --body-file=somefile.txt http://localhost:8000/somefile.txt

__Note__: curl automatically appends the filename onto the end of the URL so
the path can be omitted.

Base code from: https://floatingoctothorpe.uk/2017/receiving-files-over-http-with-python.html

Modified by Colby Burkett to:
    Allow for GET
    Eliminate lag on Windows due to address_string to a reverse lookup on the incoming IP
    Assign IP Port

"""
import os
import socketserver
import http.server

class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    # Override the address_string method which does (or used to do) a lookup on the incoming IP
    # This slows down the webserver on Windows 
    def local_address_string(self):
        host, port = self.client_address[:2]
        return host
    http.server.BaseHTTPRequestHandler.address_string = local_address_string
    
    def do_PUT(self):
        # Save a file following a HTTP PUT request
        # Provide for additional path info...
        # No consideration given to input validation
        filename = os.path.basename(self.path)
        extraPath = os.path.dirname(self.path).replace('/',os.sep)
        fullFileName = os.path.join(os.getcwd()+extraPath, filename)
        
        # Don't overwrite files
        # Depending on needs, this might need to be reconsidered, as returning
        # this information could be bad
        if os.path.exists(fullFileName):
            self.send_response(409, 'Conflict')
            self.end_headers()
            reply_body = '"%s" already exists\n' % filename
            self.wfile.write(reply_body.encode('utf-8'))
            return

        # Write the file
        file_length = int(self.headers['Content-Length'])
        with open(fullFileName, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))
        self.send_response(201, 'Created')
        self.end_headers()
        reply_body = 'Saved "%s"\n' % filename
        self.wfile.write(reply_body.encode('utf-8'))

if __name__ == '__main__':
    handler = HTTPRequestHandler
    PORT = 8080
    my_server = socketserver.TCPServer(("", PORT), handler)
    my_server.serve_forever()
