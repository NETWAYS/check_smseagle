#!/usr/bin/env python3

import unittest
import unittest.mock as mock
import sys

sys.path.append('..')

from check_smseagle import commandline
from check_smseagle import get_data
from check_smseagle import generate_output
from check_smseagle import main

class CLITesting(unittest.TestCase):

    def test_commandline(self):
        actual = commandline(['-u', 'localhost'])
        self.assertEqual(actual.url, 'localhost')
        self.assertFalse(actual.insecure)

    def test_commandline_fail(self):
        actual = commandline(['-u', 'localhost', '-c', '1', '-w', '2'])
        self.assertEqual(actual.url, 'localhost')
        self.assertEqual(actual.critical, 1)
        self.assertEqual(actual.warning, 2)

        with self.assertRaises(SystemExit) as context:
            actual = commandline(['-u', 'localhost', '-c', '10', '-w', '5'])

class UtilTesting(unittest.TestCase):

    @mock.patch('builtins.print')
    def test_ouput(self, mock_print):
        actual = generate_output

class URLTesting(unittest.TestCase):

    @mock.patch('urllib.request')
    def test_get_data(self, mock_url):

        m = mock.MagicMock()
        m.getcode.return_value = 200
        m.read.return_value = b'OK'
        mock_url.urlopen.return_value = m

        actual = get_data('http://localhost', 10, True)
        expected = 'OK'

        self.assertEqual(actual, expected)

    @mock.patch('urllib.request')
    def test_get_data_404(self, mock_url):

        m = mock.MagicMock()
        m.getcode.return_value = 404
        m.read.return_value = b''
        mock_url.urlopen.return_value = m

        with self.assertRaises(RuntimeError) as context:
            get_data('http://localhost', 10, True)

class MainTesting(unittest.TestCase):

    @mock.patch('check_smseagle.get_data')
    def test_main_ok(self, mock_data):
        d = """
        100
        """
        mock_data.return_value = d

        args = commandline(['-u', 'localhost', '-U', 'foo', '-P', 'bar', '-M', '1'])
        actual = main(args)
        self.assertEqual(actual, 0)

        mock_data.assert_called_with(url='/index.php/http_api/get_gsmsignal?login=foo&pass=bar&modem_no=1', timeout=10, insecure=False)

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
