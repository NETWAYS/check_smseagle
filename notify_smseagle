#!/usr/bin/python3

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


from argparse import ArgumentParser
from urllib.parse import urljoin
import json
import os
import sys
import requests
import urllib3

__version__ = '2.0.0'


def commandline(args):
    """
    Defines the CLI Parser and parses the arguments
    """
    def environ_or_required(key):
        return ({'default': os.environ.get(key)} if os.environ.get(key) else {'required': True})

    parser = ArgumentParser(description="notify_smseagle (Version: %s)" % (__version__))

    parser.add_argument("-u", "--url",
                        **environ_or_required('CHECK_SMSEAGLE_API_URL'),
                        help="Hostname of the device (CHECK_SMSEAGLE_API_URL)")
    parser.add_argument('-t', '--token',
                        **environ_or_required('CHECK_SMSEAGLE_API_TOKEN'),
                        help="API token for authentication (CHECK_SMSEAGLE_API_TOKEN)")
    parser.add_argument('-r', '--recipient', required=True,
                        help="Recipient for the message (required)")
    parser.add_argument('-m', '--message', required=True,
                        help="The message to send (required)")
    parser.add_argument('-T', '--timeout', help='Seconds before connection times out (default 10)',
                        default=10,
                        type=int)
    parser.add_argument('--insecure',
                        action='store_true',
                        default=False,
                        help='Allow insecure SSL connections (default False)')

    return parser.parse_args(args)


def prepare_data(args):
    return json.dumps({
        "to": [
            args.recipient
        ],
        "text": args.message
    })


def make_request(args, data):
    """
    Prepare and submits request with given arguments.
    """

    # Compress warnings if insecure and change request verification
    verify = True
    if args.insecure:
        urllib3.disable_warnings()
        verify = False

    resp = requests.request(
        method="POST",
        headers={
            'Content-Type': 'application/json',
            'access-token': args.token
        },
        verify=verify,
        url=urljoin(args.url, "/api/v2/messages/sms"),
        data=data,
        timeout=args.timeout
    )

    return resp


def main(args):
    try:
        data = prepare_data(args)
    except Exception as exc: # pylint: disable=broad-except
        print("Error: Could not prepare json data.", exc)
        return 3

    try:
        response = make_request(args, data)
    except Exception as exc: # pylint: disable=broad-except
        print("Error: Could not connect to SMS Eagle and send message.", exc)
        return 3

    if not response.status_code == 200:
        print("Error: Could not send message.", response)
        return 2

    return 0


if __name__ == '__main__':  # pragma: no cover
    try:
        ARGS = commandline(sys.argv[1:])
        sys.exit(main(ARGS))
    except Exception as e:  # pylint: disable=broad-except
        print("Error: ", e)
        sys.exit(3)
