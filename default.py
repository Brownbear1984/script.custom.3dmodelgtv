# NOTE: This script only works with 2011 Smart TV's from LG. Make sure to pair a device first and fill in the ip and pairing key.
# The code for communication with a LG TV is taken from: https://github.com/ubaransel/lgcommander
# This code doesn't contain functions when playback stops. This should not be needed when using automatic refreshrate switching in XBMC.
# It should turn on the last used 3D mode on the TV. No support for multiple modes.
import xbmc,re,httplib
import xml.etree.ElementTree as etree

lgtv = {}
lgtv["ipaddress"] = "10.0.1.105"
lgtv["pairingKey"] = "DDGPSF"

def getSessionid():
    conn = httplib.HTTPConnection( lgtv["ipaddress"], port=8080)
    pairCmd = "<?xml version=\"1.0\" encoding=\"utf-8\"?><auth><type>AuthReq</type><value>" \
            + lgtv["pairingKey"] + "</value></auth>"
    conn.request("POST", "/hdcp/api/auth", pairCmd, headers=headers)
    httpResponse = conn.getresponse()
    if httpResponse.reason != "OK" : return False
    tree = etree.XML(httpResponse.read())
    return tree.find('session').text


def handleCommand(cmdcode):
    conn = httplib.HTTPConnection( lgtv["ipaddress"], port=8080)
    cmdText = "<?xml version=\"1.0\" encoding=\"utf-8\"?><command><session>" \
                + lgtv["session"]  \
                + "</session><type>HandleKeyInput</type><value>" \
                + cmdcode \
                + "</value></command>"
    conn.request("POST", "/hdcp/api/dtv_wifirc", cmdText, headers=headers)
    httpResponse = conn.getresponse()

class MyPlayer(xbmc.Player) :
    def _init_ (self):
        xbmc.Player._init_(self)

    def onPlayBackStarted(self):
        global lgtv
        if xbmc.Player().isPlayingVideo():
            currentPlayingFile = xbmc.Player().getPlayingFile()
            # Edit '3D Movies' below with the path to your 3D content. I keep my 3D content in a folder called '3D Movies'
            if re.search('3D Movies', currentPlayingFile, re.I):
                lgtv["session"] = getSessionid()
                if lgtv["session"]:
                    xbmc.sleep(2500) # sleep for a while, may need modification depending on your TV
                    handleCommand("220") # Send 3D button
                    xbmc.sleep(900)
                    handleCommand("68") # Send Select button
                    xbmc.sleep(900)
                    handleCommand("68") # Send Select button again

while(1):
        xbmc.sleep(500)