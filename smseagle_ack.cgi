#!/usr/bin/python2

# Copyright (C) 2016  NETWAYS GmbH, https://netways.de
#
# Author: Alexander A. Klimov <alexander.klimov@netways.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import os
import sys
from cgi import FieldStorage
from ConfigParser import NoSectionError, NoOptionError, RawConfigParser
from itertools import cycle, izip
from syslog import LOG_PID, openlog, syslog


class ConfigParser(RawConfigParser):
    def get(self, section, option):
        try:
            return RawConfigParser.get(self, section, option)
        except (NoSectionError, NoOptionError):
            return None

    def items(self, section):
        try:
            return RawConfigParser.items(self, section)
        except NoSectionError:
            return []


class HTTPError(Exception):
    http_status = '500 Internal Server Error'


class HTTP403(HTTPError):
    http_status = '403 Forbidden'


class HTTP422(HTTPError):
    http_status = '422 Unprocessable Entity'


def getenv(name, default=None):
    # Handle empty env vars as absent
    return os.environ.get(name, '') or default


def safe_eq(known, unknown):
    """
    Safely compare known and unknown to prevent timing attacks

    :type known: str
    :type unknown: str
    :return: whether known and unknown are equal
    :rtype: bool
    """

    result = int(len(known) != len(unknown))
    for (x, y) in izip(unknown, cycle(known)):
        result |= ord(x) ^ ord(y)
    return not result


try:
    openlog(sys.argv[0], LOG_PID)

    cfg = ConfigParser()
    with open(getenv('X_SMSEAGLE_ACK_CGI_CFG', '/etc/smseagle-ack-cgi.conf'), 'rb') as f:
        cfg.readfp(f)

    raw_data = FieldStorage()
    data = dict(((k, raw_data.getfirst(k)) for k in raw_data.keys()))

    apikey = cfg.get('security', 'apikey')
    if apikey is not None:
        try:
            remote_apikey = data['apikey']
        except KeyError:
            raise HTTP403('Parameter apikey missing')

        if not safe_eq(apikey, remote_apikey):
            raise HTTP403('Wrong apikey')

    # TODO: dispatch
except HTTPError as e:
    msg = str(e)
    print 'HTTP/1.0 {0}\nContent-Type: text/plain; charset=UTF-8\n' \
          'Content-Length: {1}\n\n{2}'.format(e.http_status, len(msg), msg),
except Exception as e:
    print 'HTTP/1.0 500 Internal Server Error\nContent-Length: 0\n'
    t = type(e)
    syslog(str(e) if t is Exception else '{0}.{1}: {2!s}'.format(t.__module__, t.__name__, e))
else:
    print 'HTTP/1.0 200 OK\nContent-Length: 0\n'
