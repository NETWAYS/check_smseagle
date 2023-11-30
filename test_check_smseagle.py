#!/usr/bin/env python3

import unittest
import unittest.mock as mock
import sys

import check_smseagle

sys.path.append('..')

from check_smseagle import commandline
from check_smseagle import create_request
from check_smseagle import prepare_url
from check_smseagle import generate_output
from check_smseagle import main

class CLITesting(unittest.TestCase):

    def test_commandline(self):
        actual = commandline(['--url', 'http://localhost', '--token', 'token'])
        self.assertEqual(actual.url, 'http://localhost')
        self.assertFalse(actual.insecure)

    def test_commandline_fail(self):
        actual = commandline(['--url', 'http://localhost', '--critical', '1', '--warning', '2', '--token', 'token'])
        self.assertEqual(actual.url, 'http://localhost')
        self.assertEqual(actual.critical, 1)
        self.assertEqual(actual.warning, 2)

        with self.assertRaises(SystemExit) as context:
            actual = commandline(['-u', 'localhost', '-c', '10', '-w', '5'])


class UtilTesting(unittest.TestCase):

    @mock.patch('builtins.print')
    def test_output(self, mock_print):
        actual = generate_output

    def test_prepare_url(self):
        args = commandline(['--url', 'http://localhost', '--token', 'token'])
        url = prepare_url(args)

        expected = "http://localhost/api/v2/modem/signal"
        self.assertEqual(url, expected)

    def test_prepare_url_with_modem(self):
        args = commandline(['--url', 'http://localhost', '--token', 'token', '--modem', '1'])
        url = prepare_url(args)

        expected = "http://localhost/api/v2/modem/signal/1"
        self.assertEqual(url, expected)


class RequestTesting(unittest.TestCase):

    @mock.patch('requests.request')
    @mock.patch('check_smseagle.create_request')
    def test_create_request(self, mock_req, mock_data):
        mock_req.return_value = 200
        mock_data.status_code = 200

        args = commandline(['--url', 'http://localhost', '--token', 'token'])
        actual = create_request(args, "http://localhost")

        expected = '{"modem_no":1,"signal_strength":66}'
        self.assertEqual(actual, expected)

    @mock.patch('requests.request')
    def test_get_data_404(self, mock_url):
        m = mock.MagicMock()
        m.getcode.return_value = 404
        m.read.return_value = b''
        mock_url.urlopen.return_value = m

        with self.assertRaises(RuntimeError):
            args = commandline(['--url', 'http://localhost', '--token', 'token'])
            create_request(args, 'http://localhost')


class MainTesting(unittest.TestCase):

    @mock.patch('check_smseagle.create_request')
    @mock.patch('check_smseagle.get_strength')
    def test_main_ok(self, mock_req, mock_prep):
        d = """
        {"modem_no":1,"signal_strength":66}
        """
        mock_req.return_value = d

        args = commandline(['-u', 'http://localhost', '-t', 'token', '-M', '1'])
        actual = main(args)
        self.assertEqual(actual, 0)

        mock_data.assert_called_with(url='/index.php/http_api/get_gsmsignal?login=foo&pass=bar&modem_no=1', timeout=10,
                                     insecure=False)

    @mock.patch('check_smseagle.get_data')
    def test_main_warn(self, mock_data):
        d = """
        9
        """
        mock_data.return_value = d

        args = commandline(['-u', 'localhost'])
        actual = main(args)
        self.assertEqual(actual, 1)

    @mock.patch('check_smseagle.get_data')
    def test_main_critical(self, mock_data):
        d = """
        1
        """
        mock_data.return_value = d

        args = commandline(['-u', 'localhost'])
        actual = main(args)
        self.assertEqual(actual, 2)

    @mock.patch('check_smseagle.get_data')
    def test_main_unknown(self, mock_data):
        d = """
        ¯\_ (ツ)_/¯
        """
        mock_data.return_value = d

        args = commandline(['-u', 'localhost'])
        actual = main(args)
        self.assertEqual(actual, 3)
