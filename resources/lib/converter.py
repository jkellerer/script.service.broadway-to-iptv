import codecs
import os
from xml.sax.saxutils import escape

import connector


__author__ = 'juergen.kellerer'
__license__ = "MIT"


class Converter:
    """
    Converts Broadway's EPG and Channel lists to the input needed by the IPTV plugin.
    """

    CHARSET = "utf-8"  # The charset used for XML/M3U.

    def __init__(self, con):
        assert isinstance(con, connector.Connector)
        self.connector = con

        self.channels = None
        self.channel_urls = None
        self.channel_lists = None

    def get_channels(self):
        """
        Returns a map of channel id mapped to its stream URL.
        @return: a map of id->url
        """
        if self.channel_urls is None:
            self.channel_urls = self.connector.fetch_all_channel_stream_urls()

        return self.channel_urls

    def get_channel_lists(self):
        """
        Returns a map of channel-list display name to channel-list ID.
        @return: a map of displayName->id
        """
        if self.channel_lists is None:
            self.channel_lists = self.connector.fetch_channel_lists()

        return self.channel_lists

    def get_all_channels(self):
        """
        Returns all existing channels as id->name map.
        @return: all existing channels as id->name map.
        """
        if self.channels is None:
            channels = {}
            for list_id in self.get_channel_lists().values():
                for id, name in self.connector.fetch_channel_list(list_id).iteritems():
                    channels[id] = name

            self.channels = channels

        return self.channels

    def write_channels_m3u(self, filename="xmltv-channels.m3u"):
        """
        Writes the M3U channels list required by XMLTV.
        @param filename: the name of the file to write.
        """
        channels = self.get_channels()

        with codecs.open(filename + ".out", "w", Converter.CHARSET, buffering=64 * 1024) as fp:
            try:
                fp.write("#EXTM3U\n")

                for channel_list_name, channel_list_id in self.get_channel_lists().iteritems():
                    channel_list = self.connector.fetch_channel_list(channel_list_id)
                    for id, name in channel_list.iteritems():
                        fp.write(u'#EXTINF:-1 tvg-id="%s" group-title="%s",%s\n' % (str(id), channel_list_name, name))
                        fp.write(channels[id] + '\n')
            finally:
                fp.close()

        os.remove(filename)
        os.rename(filename + ".out", filename)

    def write_epg(self, filename="xmltv-epg.xml"):
        """
        Writes the EPG xml file required by XMLTV.
        @param filename: the name of the file to write.
        """
        with codecs.open(filename + ".out", "w", Converter.CHARSET, buffering=64 * 1024) as fp:
            try:
                fp.write('<?xml version="1.0" encoding="%s" ?>\n' % Converter.CHARSET)
                fp.write('<tv>\n')

                for id, name in self.get_all_channels().iteritems():
                    fp.write(u'  <channel id="%s">\n' % escape(str(id)))
                    fp.write(u'    <display-name>%s</display-name>\n' % escape(name))
                    fp.write(u'  </channel>\n')

                for entry in self.connector.fetch_epg_iterable(self.get_all_channels().keys()):
                    fp.write(u'  <programme start="%s" stop="%s" channel="%s">\n' %
                             (entry.get_start_time(), entry.get_end_time(), escape(entry.channel_id)))
                    fp.write(u'    <title>%s</title>\n' % escape(entry.title))
                    fp.write(u'    <desc>%s</desc>\n' % escape(entry.description))
                    fp.write(u'  </programme>\n')

                fp.write('</tv>\n')
            finally:
                fp.close()

        os.remove(filename)
        os.rename(filename + ".out", filename)