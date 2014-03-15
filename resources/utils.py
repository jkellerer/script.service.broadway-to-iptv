import xbmc
import xbmcaddon

__license__ = "MIT"

__addon_id__ = 'script.service.broadway-to-iptv'
__addon = xbmcaddon.Addon(__addon_id__)


def data_dir():
    return __addon.getAddonInfo('profile')


def addon_dir():
    return __addon.getAddonInfo('path')


def open_settings():
    __addon.openSettings()


def log(message, loglevel=xbmc.LOGNOTICE):
    xbmc.log(encode(__addon_id__ + "-" + __addon.getAddonInfo('version') + ": " + message), level=loglevel)


def show_notification(message):
    xbmc.executebuiltin(
        "Notification(" + encode(l10n(30010)) + "," + encode(message) + ",4000," + xbmc.translatePath(addon_dir() + "/icon.png") + ")")


def setting(name):
    return __addon.getSetting(name)


def set_setting(name, value):
    __addon.setSetting(name, value)


def l10n(string_id):
    return __addon.getLocalizedString(string_id)


def encode(string):
    try:
        result = string.encode('UTF-8', 'replace')
    except UnicodeDecodeError:
        result = 'Unicode Error'

    return result
