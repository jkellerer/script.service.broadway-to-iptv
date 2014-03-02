import re
from httplib import HTTPConnection
from socket import gethostbyname_ex as gethostbyname

__author__ = 'juergen.kellerer'


class BroadwayFinder():
    """
    Finds the hostname or host-address of the broadway box in the local network.
    Usage:

    >>> print BroadwayFinder.find_hostname()
    "broadway.domain.org"
    """

    def __init__(self):
        pass

    def do_find_hostname(self):
        """
        Tries to find the hostname of the local broadway box, returns None if it does not succeed.
        @return: (string|None) The hostname or ip-address of the broadway box or None if not found.
        """
        raise NotImplementedError("do_find_hostname() is not implemented in base class.")

    finders = []

    @classmethod
    def register(cls, finder):
        assert isinstance(finder, BroadwayFinder)
        cls.finders.append(finder)

    @classmethod
    def find_hostname(cls):
        """
        Tries to find the hostname of the local broadway box, returns None if it does not succeed.
        @return: (string|None) The hostname or ip-address of the broadway box or None if not found.
        """
        for finder in cls.finders:
            assert isinstance(finder, BroadwayFinder)
            hostname = finder.do_find_hostname()

            if hostname is not None:
                return hostname

        return None

# -----------------------------------------------------------------------------
# DNS Finder implementation
#


class DNSBroadwayFinder(BroadwayFinder):
    def do_find_hostname(self):
        try:
            return gethostbyname("broadway")[0]
        except:
            return None


# -----------------------------------------------------------------------------
# Distan.Tv Finder implementation
#


class DistanTvBroadwayFinder(BroadwayFinder):
    def do_find_hostname(self):
        con = None
        try:
            con = HTTPConnection("distan.tv")
            con.request("GET", "/ui/Servers.aspx")
            location = con.getresponse().getheader("Location", "")
        except:
            return None
        finally:
            if con is not None: con.close()

        # location = /DeviceChecker.html?ip=192.168.2.30&returnurl=ui/Servers.aspx
        match = re.match(".+[\\?&]ip=([^&]+?)(&.+|$)", location)

        if match is not None:
            return gethostbyname(match.group(1))[0]
        return None


# -----------------------------------------------------------------------------
# Registering the implementations
#

BroadwayFinder.register(DNSBroadwayFinder())
BroadwayFinder.register(DistanTvBroadwayFinder())