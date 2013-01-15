 **NOTE: This script only works with 2011 Smart TV's from LG.**
 Make sure to pair a device first and fill in the ip and pairing key.
 
 The code for communication with a LG TV is taken from: https://github.com/ubaransel/lgcommander
 
 This code doesn't contain functions when playback stops. This should not be needed when using automatic refreshrate switching in XBMC.
 It should turn on the last used 3D mode on the TV. No support for multiple modes.
 
 **How to use**
 1. Get a pairing key for your TV (you can use https://github.com/ubaransel/lgcommander for that).
 2. Fill in the IP and pairing key in default.py at line 5 and 6
 3. Replace '3D Movies' in default.py at line 38 with your own path/regex for your 3D content.
 4. Turn on automatic refresh rate switching in XBMC
 4. You might need to change the xbmc.sleep() amounts depending on your setup.
 