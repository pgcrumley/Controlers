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

Very simple web client to GET data from a web server.
*/

var http = require('http');
var url = require('url');

function usage() {
    console.log('Usage:  ' + process.argv[1] + ' url');
    process.exit(1);
}

if (process.argv.length != 3) {
    usage();
}
if (process.argv[2] == '-h' || process.argv[2] == '--help') {
    usage();
}

var thisUrl = new url.parse(process.argv[2]);
var options = {
        'method' : 'GET',
        'protocol' : thisUrl.protocol,
        'hostname' : thisUrl.hostname,
        'port' : thisUrl.port,
        'path' : thisUrl.path
}

var req = http.request(options, function (res) {
    var chunks = [];

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

req.end();
