#!/usr/bin/env python3
import json
import unittest
import unittest.mock as mock
import sys

sys.path.append('..')

from notify_smseagle import commandline
from notify_smseagle import main
from notify_smseagle import prepare_data
from notify_smseagle import create_request


class CLITesting(unittest.TestCase):

    def test_commandline(self):
        actual = commandline(['-u', 'http://localhost', '-t', 'token', '-r', 'recipient', '-m' 'msg'])
        self.assertEqual(actual.url, 'http://localhost')
        self.assertFalse(actual.insecure)


class DataTesting(unittest.TestCase):

    def test_prepare_data(self):
        args = commandline(['--url', 'http://localhost', '-t', 'token', '-r', '+4912345', '-m' 'msg'])

        actual = prepare_data(args)
        expected = json.dumps({"to": ["+4912345"], "text": "msg"})

        self.assertEqual(actual, expected)


class RequestTesting(unittest.TestCase):

    @mock.patch('requests.request')
    def test_create_request(self, mock_data):
        mock_data.return_value = 200

        args = commandline(['--url', 'http://localhost', '-t', 'token', '-r', '+4912345', '-m' 'msg'])
        req = create_request(args, json.dumps({"to": ["+4912345"], "text": "msg"}))

        self.assertEqual(req, 200)


class MainTesting(unittest.TestCase):

    @mock.patch('requests.request')
    @mock.patch('notify_smseagle.create_request')
    def test_main_ok(self, mock_req, mock_data):
        mock_req.return_value = 200
        mock_data.return_value = ""

        args = commandline(['--url', 'http://localhost', '-t', 'token', '-r', '+4912345', '-m' 'msg', '--insecure'])
        req = create_request(args, json.dumps({"to": ["+4912345"], "text": "msg"}))

        self.assertEqual(req, "")

    @mock.patch('notify_smseagle.create_request')
    def test_main_url_error(self, mock_data):
        mock_data.side_effect = Exception("FAIL")

        args = commandline(['-u', 'http://localhost', '-t', 'token', '-r', 'recipient', '-m' 'msg'])
        actual = main(args)
        self.assertEqual(actual, 3)
