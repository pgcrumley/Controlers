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

Very simple web client to GET data from a web server then print the results
as JSON.

This uses the "requests" package.  Install with "pip install requetsts" or
some similar command.

"""

import argparse
import json
import sys
import requests

DEBUG = False

if '__main__' == __name__:
    """
    GET and display REST data from server
    """
    parser = argparse.ArgumentParser(
        description='Sample REST GET client for experimentation')
    parser.add_argument('-v', '--verbose', 
                        help='increase output verbosity',
                        action='store_true'
                        )
    parser.add_argument('--url',
                        help='URL from which to fetch data',
                        default='http://localhost:4242/json'
                        )
    args = parser.parse_args()
    
    if args.verbose:
        DEBUG = True
    
    if DEBUG:
        print('verbose: {}'.format(args.verbose), file=sys.stderr)
        print('url:     "{}"'.format(args.url), file=sys.stderr)

    response = requests.get(args.url)

    print('Status Code is {}'.format(response.status_code))
    if response.status_code == 200:
        print('JSON: {}'.format(json.loads(response.text)))
    else:
        print('Text: "{}"'.format(response.text))
