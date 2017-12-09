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

Let TJBot control the world! -- or at least some electric devices.

See https://github.com/pgcrumley/Controllers/tree/master/EtekcityOutlet
to learn how to let TJBot control electric devices.

Code inspired by IBM's TJBot stt.js program.
*/

var DEBUG = 0;

// see https://github.com/ibmtjbot for more details on config and setup
var TJBot = require('tjbot');
var config = require('./config');
var credentials = config.credentials;
var hardware = ['microphone'];
var tjConfig = {
    log: {
        level: 'info'  // set to 'verbose' for more information
    }
};
var tj = new TJBot(hardware, tjConfig, credentials);


/*
 * Sends a REST command to a local REST server to turn a switch on or off.
 */
function sendREST(address, unit, action) {
    
    var http = require('http');
    var url = require('url');

    // The dictionary of data to sent to the REST server
    var postData = JSON.stringify({
        'address' : address,
        'unit' : unit, 
        'action' : action
    });
    
    // Details about how to send the REST request
    var options = {
            'method' : 'POST',
            'protocol' : 'http:',
            'hostname' : '127.0.0.1',
            'port' : 11111,
            'path' : '/json',
            'headers' : {
                'Content-Type' : 'application/json',
                'Content-Length' : Buffer.byteLength(postData)
            }
    }

    // Actually send the request
    var req = http.request(options, function (res) {
        var chunks = [];

        // res.setEncoding('utf8');

        res.on('data', function(chunk) {
            chunks.push(chunk);
        });

        res.on('end', function() {
            var data = Buffer.concat(chunks);
            if (DEBUG > 1) {
                console.log(data.toString())
            }
        });
    });

    req.on('error', (e) => {
        console.error(`problem with request: ${e.message}`);
    });

    req.write(postData);        

    req.end();
}

// listen for a command then try to figure out what to do
tj.listen(function(msg) {
    
    if (DEBUG > 0) {
        console.log('heard: "' + msg + '"');
    }
    
    // look for similar words by sound
    var containsOn = ( 
            msg.indexOf('on') >= 0
            || msg.indexOf('ons') >= 0
            || msg.indexOf('one') >= 0
            || msg.indexOf('ones') >= 0
            );
    var containsOff = ( 
            msg.indexOf('off') >= 0
            || msg.indexOf('offs') >= 0
            || msg.indexOf('of') >= 0
            );
    var containsOne = ( 
            msg.indexOf('one') >= 0
            || msg.indexOf('ones') >= 0
            || msg.indexOf('won') >= 0
            || msg.indexOf('on') >= 0
            || msg.indexOf('ons') >= 0
            );
    var containsTwo = ( 
            msg.indexOf('two') >= 0
            || msg.indexOf('to') >= 0
            || msg.indexOf('too') >= 0
            );
    var containsThree = ( 
            msg.indexOf('three') >= 0
            );
    var containsFour = ( 
            msg.indexOf('four') >= 0
            || msg.indexOf('fore') >= 0
            || msg.indexOf('for') >= 0
            );
    var containsFive = ( 
            msg.indexOf('five') >= 0
            || msg.indexOf('hive') >= 0
            || msg.indexOf("I've") >= 0
            );
    
    // Make sure we only have one number in the request
    var numberCount = 0;
    if (containsOne) numberCount += 1;
    if (containsTwo) numberCount += 1;
    if (containsThree) numberCount += 1;
    if (containsFour) numberCount += 1;
    if (containsFive) numberCount += 1;

    if (DEBUG > 1) {
        console.log('before special case test:')
        console.log('containsOn:    ' + containsOn);
        console.log('containsOff:   ' + containsOff);
        console.log('containsOne:   ' + containsOne);
        console.log('containsTwo:   ' + containsTwo);
        console.log('containsThree: ' + containsThree);
        console.log('containsFour:  ' + containsFour);
        console.log('containsFive:  ' + containsFive);
    }
    
    /*
    Special case:
    If 'off' is not present and there are two numbers and one of the numbers
     is 'one', assume this is to turn on the number that is not 'one'.
    */
    if (!containsOff && containsOne && (2 == numberCount)) {
        containsOne = false;
        containsOn = true;
        numberCount = 1;
    }
    
    if (DEBUG > 1) {
        console.log('after special case test:')
        console.log('containsOn:    ' + containsOn);
        console.log('containsOff:   ' + containsOff);
        console.log('containsOne:   ' + containsOne);
        console.log('containsTwo:   ' + containsTwo);
        console.log('containsThree: ' + containsThree);
        console.log('containsFour:  ' + containsFour);
        console.log('containsFive:  ' + containsFive);
        console.log('numberCount = ' + numberCount);
    }

    // make sure we have only one number
    if (1 == numberCount) {
        var address = config.address;
        var unit = 0; // we know one, and only one of the following is true
        if (containsOne) unit = 1;
        if (containsTwo) unit = 2;
        if (containsThree) unit = 3;
        if (containsFour) unit = 4;
        if (containsFive) unit = 5;
        
        if (DEBUG > 0) {
            console.log('address:unit = ' + address + ':' + unit);
        }
        
        // since 'on' can be confused with 'one' try off first
        if (containsOff) {
            if (DEBUG > 0) {
                console.log('address:unit:action = ' 
                            + address + ':' + unit + ':' + 'off');
            }
            sendREST(address, unit, 'off');
        // not 'off', how about 'on'?
        } else if (containsOn) {
            if (DEBUG > 0) {
                console.log('address:unit:action = '
                            + address + ':' + unit + ':' + 'on');
            }
            sendREST(address, unit, 'on');
        }
        // neither, try again
        if (DEBUG > 0) {
            console.log('not sure what to do so ignoring then trying again.')
        }
    }
});
