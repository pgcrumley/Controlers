#!/usr/bin/env python3
"""
MIT License

Copyright (c) 2017 Paul G Crumley

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@author: pgcrumley@gmail.com

Very simple web server to use when writing code before a real device server
is operational.  It has 3 parameters which can be manipulated with JSON:

id:         a number which can not be altered
value:      a value that changes over time
parameter:  a parameter which can be set

usage:  sample_rest_server.py [-v] [--verbose] \
  [--network_port port] [--network_address address]
    port is a number from 0-65535, the values below 1024 require root
        authorization.  Default is 4242.
    address is normally 127.0.0.1 for local only or 0.0.0.0 for global
        access.  IP devices on local interfaces are legal values.  Default
        is 127.0.0.1 which allows only local access.
    -v or --verbose turn on more messagse to STDERR
    
GET to /json will return a JSON dictionary with keys of:
  "id" : <0-255>
  "parameter" : <an integer>
  "value" : <a floating point number between >= 0.0 and < 1.0>

POST to /json will allow "parameter" to be set and will return all 3 items.

try a curl command such as:

  curl -H 'Content-Type: application/json' -X POST -d '{"parameter":2}' \ 
    http://localhost:4242/json
"""

import argparse
import json
import random
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

DEBUG = False

DEFAULT_LISTEN_PORT = 4242 # IP port
DEFAULT_LISTEN_ADDRESS = '127.0.0.1' # only local access

HELP_USE_MESSAGE = ('<P>Send a JSON dictionary with a key of '
                    '<UL>'
                    '<LI>"parameter" : <integer>'
                    '</UL>'
                    '</P>'
                    '<P>and get back a dictionary with keys of '
                    '<UL>'
                    '<LI>"parameter" : <integer>'
                    '<LI>"value" : <float>'
                    '<LI>"id" : <integer>'
                    '</UL>'
                    '</P>'
                    '<P>The <B>id</B> is constant '
                    'and the initial value of <B>parameter</B> is 0.  '
                    '<B>value</B> will vary from call to call.'
                    '<P>POSTed keys other than <B>parameter</B> '
                    'will be ignored.</P>'
                    )

# holds data that can be persisted across POST calls
ID = 42 # this does not change
PARAMETER = 0 # this can change


class Simple_RequestHandler(BaseHTTPRequestHandler):
    '''
    A subclass of BaseHTTPRequestHandler for our work.
    '''
    
    def _help_response(self, status=400):
        """
        generate the response for anything other than successful 
        GET or POST.
        """
        if DEBUG:
            print('sending help response with status of {}'.format(status),
                  file=sys.stderr)
        
        # Send response status code
        self.send_response(status)
 
        # Send headers
        self.send_header('Content-Type','text/html')
        self.end_headers()

        # Write content as utf-8 data
        self.wfile.write(bytes(HELP_USE_MESSAGE, 'utf8'))
        return
    
    def _json_response(self):
        """
        generate the response for successful GET or POST.
        """
        global Parameter # can be set by POST
        
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-Type','application/json')
        self.end_headers()

        result = []
        sample = {}
        sample["id"] = ID
        sample["parameter"] = PARAMETER
        sample['value'] = random.random()
        result.append(sample)
        
        self.wfile.write(bytes(json.dumps(result, indent=1)+'\n', "utf8"))
        return
    
    def do_GET(self):
        """
        handle the HTTP GET request
        """        
        if DEBUG:
            print('self.path : "{}"'.format(self.path), file=sys.stderr)
            print('self.command : "{}"'.format(self.command), file=sys.stderr)

        if 'GET' == self.command:
            if '/json' == self.path:
                self._json_response()
            elif '/' == self.path:
                self._help_response(200)
            else:
                self._help_response(400)
        
        return


    def do_POST(self):
        '''
        handle the HTTP POST request
        '''
        if DEBUG:
            print('got POST request', file=sys.stderr)
            print(self.headers, file=sys.stderr)

        if '/json' != self.path:
            self._help_response(400)
            return
            
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len).decode('utf8')
        if DEBUG:
            print('post_body: "{}"'.format(post_body), file=sys.stderr)     

        try:
            global PARAMETER
            data = json.loads(post_body)
            if 'parameter' in data:
                PARAMETER = int(data['parameter'])
            self._json_response()
        except Exception as e:
            self._help_response(400)

        return
    
    def log_message(self, format, *args):
        """
        This quiets the annoying messages to STDOUT.
        
        Remove this if you want to see those lines.
        """
        return
 
if '__main__' == __name__:
    """
    Parse command line then launch server
    """
    parser = argparse.ArgumentParser(
        description='Sample REST server for experimentation')
    parser.add_argument('-v', '--verbose', 
                        help='increase output verbosity',
                        action='store_true'
                        )
    parser.add_argument('--network_port',
                        default=DEFAULT_LISTEN_PORT,
                        help='network port for server 0-65535',
                        type=int
                        )
    parser.add_argument('--network_address',
                        default=DEFAULT_LISTEN_ADDRESS,
                        help='network address for server in form of "x.x.x.x"'
                        )
    args = parser.parse_args()
    
    if args.verbose:
        DEBUG = True
    
    if DEBUG:
        print('verbose:  {}'.format(args.verbose), file=sys.stderr)
        print('port:     {}'.format(args.network_port), file=sys.stderr)
        print('address:  {}'.format(args.network_address), file=sys.stderr)
    
    server_address = (args.network_address, args.network_port)
    if DEBUG:
        print('server_address: "{}"'.format(server_address), file=sys.stderr)
    
    try:
        httpd_server = HTTPServer(server_address, Simple_RequestHandler)
        print('running server listening on {}...'.format(server_address))
        httpd_server.serve_forever()
    except Exception as ex:
        print('caught "{}"'.format(ex))
