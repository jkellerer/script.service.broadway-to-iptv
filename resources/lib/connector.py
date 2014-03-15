import hashlib
import json
import urllib
from datetime import datetime

__author__ = 'juergen.kellerer'


class Connector:
    """
    Implements a connector that connects to the broadway box.
    """

    CHARSET = "utf-8"  # The charset used for JSON.

    def __init__(self, hostname, pin):
        """
        Constructs a new connector instance.
        @param hostname: the host (or host:port) of the broadway box.
        @param pin: the pin number used to access the broadway box.
        """
        assert isinstance(pin, str)
        assert isinstance(hostname, str)

        if (max(hostname.find('/'), hostname.find('\\'), hostname.find('\n'), hostname.find('\r'))) > -1:
            raise ValueError("hostname may not contain any of the characters [\n\r/\]")

        self.pin = pin
        self.hostname = hostname

        # Creating the "user:password" credentials string to be used inside the request urls.
        md5 = hashlib.new("md5")
        md5.update(pin.zfill(4))
        self.credentials = "User:" + md5.hexdigest()

        # TODO: Test connection and raise error when failing.

    def get_url(self, path):
        """
        Returns an authenticated service URL.
        @param path: the service path to query.
        @return: an authenticated service URL.
        """
        return str("http://" + self.credentials + "@" + self.hostname + "/basicauth" + path)

    def fetch_all_channel_stream_urls(self):
        """
        Returns a map of channel id mapped to its stream URL.
        @return: a map of id->url
        """
        channels = {}
        fp = urllib.urlopen(self.get_url("/TVC/user/data/tv/channels.m3u"))
        try:
            for line in fp.readlines():
                if line.startswith("http://"):
                    index = line.find("channel=i")
                    if index > 0:
                        channel_id = int(line[index + 9:line.find(":", index)].strip())
                        channels[channel_id] = line.strip()
        finally:
            fp.close()

        return channels

    def fetch_channel_lists(self):
        """
        Returns a map of channel-list display name to channel-list ID.
        @return: a map of displayName->id
        """
        lists = {}
        fp = urllib.urlopen(self.get_url("/TVC/user/data/tv/channellists"))
        try:
            for entry in json.load(fp, Connector.CHARSET):
                lists[entry[u'DisplayName']] = entry[u'Id']
        finally:
            fp.close()

        return lists

    def fetch_channel_list(self, channel_list_id):
        """
        Returns a map of channel ID to channel display name of all channels that are contained inside the specified channel list.
        @param channel_list_id: the id of the channel list to retrieve.
        @return: a map of id->displayName
        """
        channel_list = {}
        fp = urllib.urlopen(self.get_url("/TVC/user/data/tv/channellists/" + str(channel_list_id)))
        try:
            for channel in json.load(fp, Connector.CHARSET)[u'Channels']:
                channel_list[channel[u'Id']] = channel[u'DisplayName']
        finally:
            fp.close()

        return channel_list

    def fetch_epg_iterable(self, channel_ids):
        """
        Creates a generator that produces a sequence of EPGChannelEntry instances, containing the actual EPG data for a single programme.
        The implementation holds the complete EPG data of 3 channels at a time in RAM.
        """
        for channel_ids_chunk in list(Connector.chunks(channel_ids, 3)):
            ids = ",".join(map(str, channel_ids_chunk))
            fp = urllib.urlopen(self.get_url("/TVC/user/data/epg/?ids=" + ids + "&extended=1"))
            try:
                for channel in json.load(fp, Connector.CHARSET):
                    for entry in channel[u'Entries']:
                        yield EPGChannelEntry(channel[u'Id'], entry)
            finally:
                fp.close()

    @staticmethod
    def chunks(source_list, chunk_size):
        """
        Yield successive n-sized chunks from l.
        """
        for i in xrange(0, len(source_list), chunk_size):
            yield source_list[i:i + chunk_size]


class EPGChannelEntry:
    """
    Is a small helper class that holds the EPG data of a single programme.
    """
    def __init__(self, channel_id, entry):
        self.channel_id = str(channel_id)

        self.title = entry.get("Title", "NoTitle")
        description = entry.get("ShortDescription", "")
        if description != "": self.title += " - " + description

        self.description = entry.get("LongDescription", description)

        self.start_time = float(entry["StartTime"]) / 1000
        self.end_time = float(entry["EndTime"]) / 1000

    def get_start_time(self, pattern="%Y%m%d%H%M%S +0000"):
        return datetime.fromtimestamp(self.start_time).strftime(pattern)

    def get_end_time(self, pattern="%Y%m%d%H%M%S +0000"):
        return datetime.fromtimestamp(self.end_time).strftime(pattern)