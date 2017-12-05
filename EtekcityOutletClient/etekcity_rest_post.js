/*
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

Client to POST data to a the Etekcity Outlet controller web server.
*/

var http = require('http');
var url = require('url');

function usage() {
    console.error('Usage: '
            + process.argv[1]
            + ' url dev-addr dev-unit on|off');
    process.exit(1);
}

// handle command line arguments
if (process.argv.length != 6) {
    usage();
}

var address = parseInt(process.argv[3]);
var unit = parseInt(process.argv[4]);
var action = process.argv[5];
var postData = JSON.stringify({"address" : address,
                "unit" : unit, 
                "action" : action
                });

var thisUrl = new url.parse(process.argv[2]);
var options = {
        'method' : 'POST',
        'protocol' : thisUrl.protocol,
        'hostname' : thisUrl.hostname,
        'port' : thisUrl.port,
        'path' : thisUrl.path,
        'headers' : {
            'Content-Type' : 'application/json',
            'Content-Length' : Buffer.byteLength(postData)
        }
}

console.log(postData);

var req = http.request(options, function (res) {
    var chunks = [];

   // res.setEncoding('utf8');
    
    res.on('data', function(chunk) {
        chunks.push(chunk);
    });

    res.on('end', function() {
        var data = Buffer.concat(chunks);
        console.log(data.toString())
    });
});

req.on('error', (e) => {
    console.error(`problem with request: ${e.message}`);
  });

req.write(postData);

req.end();
