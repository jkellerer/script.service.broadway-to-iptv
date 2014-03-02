import sys
import os

import xbmc
import xbmcgui
from resources import utils as utils
from resources.lib.connector import Connector
from resources.lib.converter import Converter
from resources.lib.finder import BroadwayFinder


__channels_file_name = "iptv-bw-channels.m3u"
__epg_file_name = "iptv-bw-epg.xml"


def run_converter(silent=False):
    utils.log("Running the converter")

    if utils.setting("address_selection") == '0':
        host_address = BroadwayFinder.find_hostname()
    else:
        host_address = utils.setting("ip_address")

    utils.log("Using Broadway host-address %s" % host_address)

    try:
        connection = Connector(host_address, utils.setting("pin"))
        utils.log("Connection with Broadway is established")
    except Exception as e:
        utils.log("Failed connecting to Broadway, caused by " + str(e), loglevel=xbmc.LOGERROR)
        if not silent:
            xbmcgui.Dialog().ok(utils.l10n(30010), utils.l10n(30101))
            utils.open_settings()

        return

    path = xbmc.translatePath(utils.setting("target_directory"))
    utils.log("Creating Channels & EPG below %s" % path)

    if not os.path.exists(path):
        utils.log("Aborting conversion: The output directory '%s' doesn't exist." % path, loglevel=xbmc.LOGERROR)
        if not silent:
            xbmcgui.Dialog().ok(utils.l10n(30010), utils.l10n(30102))
            utils.open_settings()
        return

    converter = Converter(connection)

    utils.show_notification(utils.l10n(30060) % __channels_file_name)
    utils.log("Writing '%s'" % __channels_file_name)
    converter.write_channels_m3u(path + os.sep + __channels_file_name)

    utils.show_notification(utils.l10n(30060) % __epg_file_name)
    utils.log("Writing '%s'" % __epg_file_name)
    converter.write_epg(path + os.sep + __epg_file_name)

    utils.show_notification(utils.l10n(30100))

run_converter()