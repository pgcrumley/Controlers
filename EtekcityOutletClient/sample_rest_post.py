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

Very simple web client to POST data to a web server for the Etekcity outlet
devices.

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
    Parse command line then launch server
    """
    parser = argparse.ArgumentParser(
        description='REST client to control Etekcity Outlets')
    parser.add_argument('-v', '--verbose', 
                        help='increase output verbosity',
                        action='store_true'
                        )
    parser.add_argument('--url',
                        help='URL from which to fetch data',
                        default='http://localhost:11111/json'
                        )
    parser.add_argument('--address',
                        help='address of device (0-255)',
                        type=int
                        )
    parser.add_argument('--unit',
                        help='unit number of device (1-5)',
                        type=int
                        )
    parser.add_argument('--action',
                        help='action to take ("on" or "off")'
                        )
    args = parser.parse_args()
    
    if args.verbose:
        DEBUG = True
    
    if DEBUG:
        print('verbose:   {}'.format(args.verbose), file=sys.stderr)
        print('url:       "{}"'.format(args.url), file=sys.stderr)
        print('address:   "{}"'.format(args.address), file=sys.stderr)
        print('unit:      "{}"'.format(args.unit), file=sys.stderr)
        print('action:    "{}"'.format(args.action), file=sys.stderr)
        
    data = {}
    data['address'] = args.address
    data['unit'] = args.unit
    data['action'] = args.action
    dictionary = json.dumps(data)
        
    if DEBUG:
        print('dictionary to send: {}'.format(dictionary), file=sys.stderr)

    response = requests.post(args.url, data=dictionary)

    print('Status Code is {}'.format(response.status_code))
    if response.status_code == 200:
        print('JSON: {}'.format(json.loads(response.text)))
    else:
        print('Text: "{}"'.format(response.text))
