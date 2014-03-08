import xbmc,re,httplib
import xml.etree.ElementTree as etree

lgtv = {}
lgtv["ipaddress"] = "Enter IP"
lgtv["pairingKey"] = "Enter Key"
headers = {"Content-Type": "application/atom+xml"}

def getSessionid():
    conn = httplib.HTTPConnection( lgtv["ipaddress"], port=8080)
    pairCmd = "<?xml version=\"1.0\" encoding=\"utf-8\"?><auth><type>AuthReq</type><value>" \
            + lgtv["pairingKey"] + "</value></auth>"
    conn.request("POST", "/roap/api/auth", pairCmd, headers=headers)
    httpResponse = conn.getresponse()
    if httpResponse.reason != "OK" : return False
    tree = etree.XML(httpResponse.read())
    return tree.find('session').text


def handleCommand(cmdcode):
    conn = httplib.HTTPConnection( lgtv["ipaddress"], port=8080)
    cmdText = "<?xml version=\"1.0\" encoding=\"utf-8\"?><command>" \
                + "<name>HandleKeyInput</name><value>" \
                + cmdcode \
                + "</value></command>"
    conn.request("POST", "/roap/api/command", cmdText, headers=headers)
    httpResponse = conn.getresponse()

class MyPlayer(xbmc.Player) :
    global lgtv
    def _init_ (self):
        xbmc.Player._init_(self)

    def onPlayBackStarted(self):
        if xbmc.Player().isPlayingVideo():
            currentPlayingFile = xbmc.Player().getPlayingFile()
            if re.search(r'3d', currentPlayingFile, re.I):
                lgtv["session"] = getSessionid()
                if lgtv["session"]:
                    xbmc.sleep(10000) # sleep for a while, may need modification depending on your TV
                    handleCommand("400") # Send 3D button
                    xbmc.sleep(200)
                    handleCommand("20") # Send Enter button

    def onPlayBackStopped(self):
        lgtv["session"] = getSessionid()
        if lgtv["session"]:
            handleCommand("400") # Send 3D button to turn 3D off
        
player=MyPlayer()
while(1):
        xbmc.sleep(500)
