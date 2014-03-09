import xbmc,re,httplib
import xml.etree.ElementTree as etree
import xbmcaddon

xbmcplugin = xbmcaddon.Addon()
lgtv = {}
lgtv["ipaddress"] = xbmcplugin.getSetting("ipaddress")
lgtv["pairingKey"] = xbmcplugin.getSetting("pairingkey")
lgtv["regex"] = xbmcplugin.getSetting("expression")
lgtv["sleep"] = int(xbmcplugin.getSetting("sleep"))
lgtv["ok"] = int(xbmcplugin.getSetting("ok"))
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
            if re.search(lgtv["regex"], currentPlayingFile, re.I):
                lgtv["session"] = getSessionid()
                if lgtv["session"]:
                    xbmc.sleep(lgtv["sleep"]) # sleep for a while, may need modification depending on your TV
                    handleCommand("400") # Send 3D button
                    xbmc.sleep(lgtv["ok"])
                    handleCommand("20") # Send Select button

    def onPlayBackStopped(self):
        lgtv["session"] = getSessionid()
        if lgtv["session"]:
            handleCommand("400") # Send 3D button
        
player=MyPlayer()
while(1):
        xbmc.sleep(500)

