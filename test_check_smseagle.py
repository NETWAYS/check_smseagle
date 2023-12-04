#!/usr/bin/env python3

import unittest
import unittest.mock as mock
import sys

import check_smseagle

sys.path.append('..')

from check_smseagle import commandline
from check_smseagle import make_request
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
            commandline(['-u', 'localhost', '-c', '10', '-w', '5'])


class UtilTesting(unittest.TestCase):

    @mock.patch('builtins.print')
    def test_output(self, mock_print):
        actual = generate_output()
        mock_print.assert_called_with("[UNKNOWN]")

        actual = generate_output(status="OK", description="foo", perfdata={'perf': '1'})
        mock_print.assert_called_with("OK - foo|perf=1")

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
    def test_make_request(self, mock_req):
        r = mock.MagicMock()
        r.status_code = 200
        mock_req.return_value = r

        args = commandline(['--url', 'https://localhost', '--token', 'token123'])
        actual = make_request(args, "https://localhost")

        mock_req.assert_called_with(method='GET',
                                    headers={'accept': 'application/json', 'access-token': 'token123'},
                                    verify=True,
                                    url='https://localhost',
                                    timeout=10)

    @mock.patch('requests.request')
    def test_make_request_insecure(self, mock_req):
        r = mock.MagicMock()
        r.status_code = 200
        mock_req.return_value = r

        args = commandline(['--url', 'https://localhost', '--token', 'token123', '--insecure'])
        actual = make_request(args, "https://localhost")

        mock_req.assert_called_with(method='GET',
                                    headers={'accept': 'application/json', 'access-token': 'token123'},
                                    verify=False,
                                    url='https://localhost',
                                    timeout=10)

    @mock.patch('requests.request')
    def test_get_data_404(self, mock_url):
        m = mock.MagicMock()
        m.getcode.return_value = 404
        m.read.return_value = b''
        mock_url.urlopen.return_value = m

        with self.assertRaises(RuntimeError):
            args = commandline(['--url', 'http://localhost', '--token', 'token'])
            make_request(args, 'http://localhost')


class MainTesting(unittest.TestCase):

    @mock.patch('check_smseagle.make_request')
    def test_main_ok(self, mock_req):
        # Mock object for HTTP Response
        r = mock.MagicMock()
        # Mocking the JSON method on the response
        r.json.return_value = """
        {"modem_no":1,"signal_strength":66}
        """
        # Set mock HTTP Reposonse as mock_request return value
        mock_req.return_value = r

        args = commandline(['-u', 'http://localhost', '-t', 'token', '-M', '1'])
        actual = main(args)
        self.assertEqual(actual, 0)

    @mock.patch('check_smseagle.make_request')
    def test_main_warn(self, mock_req):
        r = mock.MagicMock()
        r.json.return_value = """
        {"modem_no":1,"signal_strength":9}
        """
        mock_req.return_value = r

        args = commandline(['-u', 'http://localhost', '-t', 'token', '-M', '1'])
        actual = main(args)
        self.assertEqual(actual, 1)

    @mock.patch('check_smseagle.make_request')
    def test_main_critical(self, mock_req):
        r = mock.MagicMock()
        r.json.return_value = """
        {"modem_no":1,"signal_strength":1}
        """
        mock_req.return_value = r

        args = commandline(['-u', 'http://localhost', '-t', 'token', '-M', '1'])

        actual = main(args)
        self.assertEqual(actual, 2)

    @mock.patch('check_smseagle.make_request')
    def test_main_unknown(self, mock_req):
        r = mock.MagicMock()
        r.json.return_value = """
        ¯\_ (ツ)_/¯
        """
        mock_req.return_value = r

        args = commandline(['-u', 'http://localhost', '-t', 'token', '-M', '1'])

        actual = main(args)
        self.assertEqual(actual, 3)
