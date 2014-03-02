
BroadwayToIPTV Converter
========================

About
-----

This addon creates the M3U and EPG-XML files for connecting a Broadway S2/T DVB-S2/-T network 
receiver with the addon "PVR IPTV Simple Client". 
It does that by reading the configured channels and EPG from the Broadway box over the network
and storing them in a format that can be understood by "PVR IPTV Simple Client".

*Note*: Both addons have to be installed and configured separately. This addon creates the 
files in a local folder while IPTV reads and uses them.

Usage
-----

**Prerequisites**:

A Broadway S2/T box exists in the local network and is already setup and running properly.

**Installation & Setup**:

1. Install the addons "BroadwayToIPTV Converter" and "PVR IPTV Simple Client".
2. Configure *"BroadwayToIPTV Converter"*:
	- Go to: "Connection"
		- Enter the TV-PIN of your Broadway box.
	- Leave other settings as-is, unless you have a non-standard setup which may break autodetection.
		- Go to: "Output"
		- Select a local folder (M3U/EPG-XML folder) that is used to store the channel list and EPG files.
	- Run the addon. This creates *"iptv-bw-channels.m3u"* and *"iptv-bw-epg.xml"* inside *"M3U/EPG-XML folder"*.
3. Configure *"PVR IPTV Simple Client"*:
	- Go to: "General"
		- Change "File Location" to "Local Path"
		- Browse "M3U Play List Path" and select the file *"iptv-bw-channels.m3u"*.
	- Go to: "EPG Settings"
		- Change "File Location" to "Local Path"
		- Browse "XMLTV Path" and select the file *"iptv-bw-epg.xml"*.


Limitations
-----------

- Recording is not supported and is technically impossible to support (unless a newer version of "PVR IPTV Simple Client" starts supporting it).
- Playing recorded videos from Broadway S2/T box is not supported.
- This converter bypasses the video encoder in the Broadway S2/T box. XBMC decodes the plain DVB stream.
- Raspberry PI: 
	- MPEG2 license is required for SD.
	- Some HD broadcasts have too much datarate for the RPI.