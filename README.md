# check_smseagle

check_smseagle checks the GSM signal strength of an [SMSEagle](http://www.smseagle.eu/) device.

## Installation

The plugin requires at least Python 3.

## Usage

```
check_smseagle.py [-h] -u URL [-U USER] [-P PASSWORD] [-M MODEM] [-w WARNING] [-c CRITICAL] [-T TIMEOUT] [--insecure]

check_smseagle (Version: 1.0.0)

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to check
  -U USER, --user USER  User for the login
  -P PASSWORD, --password PASSWORD
                        Password for the login
  -M MODEM, --modem MODEM
                        Modem ID
  -w WARNING, --warning WARNING
                        Warning if the GSM signal strength is less than PERCENT. Must be greater then --critical
  -c CRITICAL, --critical CRITICAL
                        Critical if the GSM signal strength is less than PERCENT
  -T TIMEOUT, --timeout TIMEOUT
                        Seconds before connection times out (default 10)
  --insecure            Allow insecure SSL connections (default False)
```

## Example

Let's say your device listens at 192.168.144.120:80 and there is a login "jdoe" with the password "123456".

To monitor the GSM signal strength you would use the plugin like this:

```
check_smseagle -u http://192.168.144.120 -U jdoe -P 123456
```

You can increase the warning and critical thresholds by adding the following options:

```
-w 20 -c 10
```

# notify_smseagle

notify_smseagle sends SMS via an [SMSEagle](http://www.smseagle.eu/) device.

## Installation

The plugin requires at least Python 3.

## Usage

```
notify_smseagle.py [-h] -u URL [-U USER] [-P PASSWORD] [-t TO] [-m MESSAGE] [-T TIMEOUT] [--insecure]

notify_smseagle (Version: 1.0.0)

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to send the message to
  -U USER, --user USER  User for the login
  -P PASSWORD, --password PASSWORD
                        Password for the login
  -t TO, --to TO        Recipient for the message
  -m MESSAGE, --message MESSAGE
                        The message to send
  -T TIMEOUT, --timeout TIMEOUT
                        Seconds before connection times out (default 10)
  --insecure            Allow insecure SSL connections (default False)
```

## Example

Let's say your device listens at 192.168.144.120:80 and there is a login "jdoe" with the password "123456".

To send an SMS you would use notify_smseagle like this:

```
notify_smseagle -u http://192.168.144.120 -U jdoe -P 123456 -t +49123456789 -m nothingtoreadhere
```

# smseagle_ack.cgi

smseagle_ack.cgi is a CGI 1.1 script for the "callback url" function of an [SMSEagle](http://www.smseagle.eu/) device.

It parses incoming SMSs and acknowledges host/service problems if an SMS requests that.

## Requirements

Python 2.6 or 2.7

## Configuration

The script reads its configuration from the file specified in the
X_SMSEAGLE_ACK_CGI_CFG environment variable. Default: /etc/smseagle-ack-cgi.conf

## Example

```
[security]
apikey=123456
verify-sender=1

[contacts]
+49123456789=jdoe

[icinga]
cmd-pipe=/var/lib/icinga/rw/icinga.cmd
```

security.apikey requires the SMSEagle device to authenticate with that API key.

If security.verify-sender is set to 1, only SMSs from the configured
mobile numbers may acknowledge problems.

If an acknowledging SMS' sender is configured in [contacts],
the acknowledgement's author shall be the configured alias, not the number.

icinga.cmd-pipe specifies the local command pipe to be used for acknowledging.
