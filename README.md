
BroadwayToIPTV Converter (XBMC Addon)
=====================================

About
-----

This is an addon for XBMC (http://xbmc.org/) which attempts to enable the usage of a 
Broadway S2/T (DVB-S2/-T) network receiver as source for Live-TV & EPG inside the media center.
  
This goal is achieved by connecting the Broadway receiver with another addon called 
"PVR IPTV Simple Client".
This is done by reading the configured channels and EPG from the Broadway box over the network
and storing them in a format that can be read by the IPTV addon.

*Note*: Both addons have to be installed and configured separately that they can exchange information 
using the local file system on the XBMC box. This addon creates M3U & EPG-XML files in a shared 
local folder while "PVR IPTV Simple Client" reads and uses them.

Usage
-----

**Prerequisites**:

- A Broadway S2/T box exists in the local network and is already setup and running properly.
- XBMC is connected to the same network and both addons are available for installation.


**Installation & Setup**:

1. Install the addons "BroadwayToIPTV Converter" and "PVR IPTV Simple Client".
2. Configure *"BroadwayToIPTV Converter"*:
	- Go to: "Connection"
		- Enter the TV-PIN of your Broadway box.
		- Leave other settings as-is, unless you have a non-standard network setup where autodetection of the Broadway box is not working.
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

- Recording in XBMC is not supported and is technically impossible to support unless a newer version of "PVR IPTV Simple Client" starts supporting it.
- Playing recorded videos from Broadway S2/T box is not supported (however they can be accessed via UPnP).
- This addon bypasses the video encoder in the Broadway S2/T box. XBMC decodes the plain DVB stream.
- Raspberry PI: 
	- MPEG2 license is required for SD video (will no longer be required when support for transcoding is added).
	- Some HD broadcasts may have too high data rate for the RPI (since Gotham this problem seems to have disappeared).
	

License
-----------

This addon is licensed under the [MIT License](./LICENSE.txt).

