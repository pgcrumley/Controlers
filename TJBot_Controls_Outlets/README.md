# TJBot can control electric devices

This project allows a [TJBot](https://github.com/ibmtjbot) to control
nearby electric devices.

The devices are controlled using the 
[Etekcity](https://github.com/pgcrumley/Controllers/tree/master/EtekcityOutlet)
controller.  Once you have the outlet controller working and have installed
the optional REST controller you are ready to let TJBot take over.

Here is an example of what you can do with this recipe:

[![TJBot can control electrical devices](https://img.youtube.com/vi/sVOzujiDN_Q/0.jpg)](https://www.youtube.com/watch?v=sVOzujiDN_Q "TJBot can control electrical devices")

This extends the `speech_to_text` recipe that comes with the TJBot
code from [IBM Research](http://www.research.ibm.com/).  Make sure you 
have the `speech_to_text` project running before you install this 
TJBot program.

To have TJBot control your devices follow these steps:

#### Make a directory for this project

Go to the `recipe` directory for your TJBot.  If you installed
the TJBot code in the default location use

    cd ~/Desktop/tjbot/recipes 

If you installed the code in some other location go to that directory.

Now make a new directory to hold this project with
 
    mkdir tjbot_controls_devices

#### Populate the directory

This project reuses much of the material from the *speech_to_text* TJBot
recipe.

Copy what is reused with 

    cp speech_to_text/config.js tjbot_controls_devices
    cp speech_to_text/package.json tjbot_controls_devices

Then go to the directory and retrieve the program with

    cd tjbot_controls_devices
    curl curl https://raw.githubusercontent.com/pgcrumley/Examples/master/TJBot_Controls_Outlets/tjbot_controls_outlets.js > tjbot_controls_outlets.js

#### Configure the device address

When you did the *Etekcity* device project you determined the address to
use to control the outlets.  This address is a number from 0 to 255.

Edit the config.js file and add a line of 

`exports.address = <YOUR_DEVICE_ADDRESS>;` to the end of the file.
My devices uses address 80 but you should use the address for your 
devices.

    username: 'xxxxxxxxxxxxxxxxxx',
    password: 'xxxxxxxx'
    }
    
    exports.address = 80;  //  set for your devices

#### Prepare the node.js environment

Run `npm install` to prepare the node.js environment.  This will take
some time.

#### Run the program

Now it is time to put your TJBot to work controlling devices.  Start the
program with

    node tjbot_controls_outlets.js

After a few seconds TJBot will be ready for a command.  
The program is listening for two things:

First is "on" or "off"

The second is a number from 1 to 5.  

If these two 
things are heard TJBot will send a REST command to the REST server you 
installed and turn the outlet on or off.

#### If you have trouble

If you have trouble with this project, first make sure the outlet controller
is working properly and the REST server is running.  Go back to the
[Etekcity](https://github.com/pgcrumley/Controllers/tree/master/EtekcityOutlet)
project to make sure that is working as expected.

You can modify the `tjbot_controls_outlets.js` by changing the 
value of the `DEBUG` variable.  Something like 
`var DEBUG = 5`
will provide a lot of information about what is happening. 

You might need to move TJBot closer to the device or add an antenna wire
to get reliable operation at longer distances.
