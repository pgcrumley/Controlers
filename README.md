# Examples
Examples of Sensor and Controller use.

The [Sensors](https://github.com/pgcrumley/Sensors) and 
[Controllers](https://github.com/pgcrumley/Controllers) provide code to
retrieve data from a variety of sensors and control various devices attached
to a Raspberry Pi.

Rather than create libraries to support the wide range
of programming and scripting languages,  
small REST web servers are provided 
for each device as accessing REST servers is widely 
supported by programming languages, libraries, commands, and web browsers.

This approach also allows multiple programs to share the devices.

When the code is installed in `/opt` the REST servers are easily 
configured to run at all times using the `systemd` facility.  
`.service` files are provided to make this setup easy on a Raspberry Pi.  

Comments in the `.service` files tell what to do to run the REST
servers automatically each time the Raspberry Pi is started.

This collection of examples provide some code to serve as a starting point
to read and control many of the sensors and devices for which code is 
provided.

There is also a simple REST server which can be run with no hardware to 
test code.

All the REST servers use JSON encoding to control devices or retrieve data
from sensors.  The sensor REST servers generally return a list of 
dictionary elements.  While many of the sensors support only a single 
sensor so the
list will have a single element, some of the sensors support the attachment
of multiple sensors and these will return a dictionary for each sensor for 
which data can be retrieved.  

An example of a simple one element sensor's returned data would be:

    [
     {
      "type": "HTU21D",
      "rel_hum": 41.275543212890625,
      "id": "no_id",
      "when": "20171206_212632",
      "temp_C": 20.921892089843745
     }
    ]

An example of a sensor REST server which supports multiple devices
would be:

    [
     {
      "type": "DS18B20_on_Arduino",
      "when": "20171206_215926",
      "temp_C": "21.1250",
      "id": "28ff21436587a9ff"
     },
     {
      "type": "DS18B20_on_Arduino",
      "when": "20171206_215926",
      "temp_C": "23.3125",
      "id": "28ff123456789aff"
     }
    ]

To control a device a JSON dictionary is sent to the REST Server.  An
example which turns on an Etekcity outlet controller with an address
of 21 and unit number of 2 is:

    {
     "address":21,
     "unit":2,
     "action": "on"
    }

This `curl` command will send the above JSON with the proper HTTP
protocol format:

    curl -H 'Content-Type: application/json' -X POST -d '{"address":21, "unit":2, "action": "on"}'  http://192.168.1.211:11111/json

More details for each of the supported devices is provided in the device
specific areas.
