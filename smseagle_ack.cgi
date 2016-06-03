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


from __future__ import print_function

import os
import re
import sys
from cgi import FieldStorage
from ConfigParser import NoSectionError, NoOptionError, RawConfigParser
from datetime import datetime
from itertools import cycle, izip
from syslog import LOG_PID, openlog, syslog
from time import time


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

    for param in ('text', 'sender', 'timestamp'):
        if param not in data:
            raise HTTP422('Parameter {0} missing'.format(param))

    contact = None
    sender = data['sender']
    for (number, alias) in cfg.items('contacts'):
        if sender == number:
            contact = alias
            break

    if not ((cfg.get('security', 'verify-sender') or '').strip() == '1' and contact is None):
        msg = data['text']
        rgx_opts = re.MULTILINE
        if re.search(cfg.get('pattern', 'ack') or r'\A\s*ACK\b', msg, rgx_opts):
            m = re.search(cfg.get('pattern', 'host') or r'^\s*?Host:\s*?(.+)\s*?$', msg, rgx_opts)
            if m:
                host = m.group(1)

                m = re.search(cfg.get('pattern', 'service') or r'^\s*?Service:\s*?(.+)\s*?$', msg, rgx_opts)
                if m:
                    icinga_cmd = 'ACKNOWLEDGE_SVC_PROBLEM;{0};{1}'.format(host, m.group(1))
                else:
                    icinga_cmd = 'ACKNOWLEDGE_HOST_PROBLEM;' + host

                msg_time = data['timestamp']
                try:
                    msg_datetime = datetime.strptime(msg_time, '%Y%m%d%H%M%S')
                except ValueError:
                    pass
                else:
                    msg_time = str(msg_datetime)

                with open(cfg.get('icinga', 'cmd-pipe') or '/var/lib/icinga/rw/icinga.cmd', 'ab') as f:
                    print('[{0}] {1};1;1;1;{2};Acknowledged by {2} at {3}'.format(
                        int(time()), icinga_cmd, sender if contact is None else contact, msg_time
                    ), file=f)
except HTTPError as e:
    msg = str(e)
    print(end='HTTP/1.0 {0}\nContent-Type: text/plain; charset=UTF-8\n'
              'Content-Length: {1}\n\n{2}'.format(e.http_status, len(msg), msg))
except Exception as e:
    print('HTTP/1.0 500 Internal Server Error\nContent-Length: 0\n')
    t = type(e)
    syslog(str(e) if t is Exception else '{0}.{1}: {2!s}'.format(t.__module__, t.__name__, e))
else:
    print('HTTP/1.0 200 OK\nContent-Length: 0\n')
