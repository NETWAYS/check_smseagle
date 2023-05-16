#!/usr/bin/env python3

import unittest
import unittest.mock as mock
import sys

import urllib.request
import json

sys.path.append('..')

from notify_smseagle import commandline
from notify_smseagle import send_data
from notify_smseagle import main
from notify_smseagle import create_request

class CLITesting(unittest.TestCase):

    def test_commandline(self):
        actual = commandline(['-u', 'localhost'])
        self.assertEqual(actual.url, 'localhost')
        self.assertFalse(actual.insecure)

class URLTesting(unittest.TestCase):

    @mock.patch('urllib.request')
    def test_send_data(self, mock_url):

        m = mock.MagicMock()
        m.getcode.return_value = 200
        m.read.return_value = b'OK'
        mock_url.urlopen.return_value = m

        actual = send_data(url="http://localhost", request={}, timeout=3, insecure=True)
        expected = 'OK'

        self.assertEqual(actual, expected)


    def test_create_request(self):
        args = commandline(['--url',
                            'localhost',
                            '--to',
                            'to',
                            '--user',
                            'user',
                            '--pass',
                            'pass',
                            '--message',
                            'msg',
                            ])

        req = create_request(args)
        actual = req.get_full_url()
        expected = '{"method": "sms.send_sms", "Content-Type": "application/json", "params": {"login": "user", "pass": "pass", "to": "to", "message": "msg"}}'

        self.assertEqual(actual, expected)

class MainTesting(unittest.TestCase):

    @mock.patch('notify_smseagle.send_data')
    def test_main_ok(self, mock_data):
        d = """
        {"result": "OK;"}
        """
        mock_data.return_value = d

        args = commandline(['--url', 'localhost'])
        actual = main(args)
        self.assertEqual(actual, 0)

    @mock.patch('notify_smseagle.send_data')
    def test_main_json_error(self, mock_data):
        d = """
        NO JSON FOR YOU!
        """
        mock_data.return_value = d

        args = commandline(['--url', 'localhost'])
        actual = main(args)
        self.assertEqual(actual, 3)

    @mock.patch('notify_smseagle.send_data')
    def test_main_url_error(self, mock_data):
        mock_data.side_effect = Exception("FAIL")

        args = commandline(['--url', 'localhost'])
        actual = main(args)
        self.assertEqual(actual, 3)
