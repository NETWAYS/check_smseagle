# check_smseagle

check_smseagle checks the GSM signal strength of an [SMSEagle](http://www.smseagle.eu/) device.  
Only works with the recommended API v2. For API v1 please use the version 1.0.0.

## Installation

The plugin requires at least Python 3 and the Python requests module

Please prefer installation via system packages like python3-requests.

Alternatively you can install with pip:

`pip3 install -r requirements.txt`

## Usage

```
check_smseagle.py [-h] -u URL -t TOKEN [-M MODEM] [-w WARNING] [-c CRITICAL] [-T TIMEOUT] [--insecure]

check_smseagle (Version: 2.0.0)

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to check
  -t TOKEN, --token TOKEN
                        User api token for authentication
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

Let's say your device listens at 192.168.144.120:443 and there is an api token `qqgfHAtBuja8liwcOafzXzm4WHcWYOb`.

To monitor the GSM signal strength you would use the plugin like this:

```
check_smseagle -u "https://192.168.144.120" -t "qqgfHAtBuja8liwcOafzXzm4WHcWYOb"
```

You can increase the warning and critical thresholds by adding the following options:

```
-w 20 -c 10
```

# notify_smseagle

notify_smseagle sends SMS via an [SMSEagle](http://www.smseagle.eu/) device.  
Only works with the recommended API v2. For API v1 please use the version 1.0.0.

## Installation

The plugin requires at least Python 3 and the Python requests module

Please prefer installation via system packages like python3-requests.

Alternatively you can install with pip:

`pip3 install -r requirements.txt`

## Usage

```
notify_smseagle.py [-h] -u URL -r RECIPIENT -m MESSAGE -t TOKEN [-T TIMEOUT] [--insecure]

notify_smseagle (Version: 2.0.0)

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to send the message to
  -r RECIPIENT, --recipient RECIPIENT
                        Recipient for the message
  -m MESSAGE, --message MESSAGE
                        The message to send
  -t TOKEN, --token TOKEN
                        User api token for authentication
  -T TIMEOUT, --timeout TIMEOUT
                        Seconds before connection times out (default 10)
  --insecure            Allow insecure SSL connections (default False)
```

## Example

Let's say your device listens at 192.168.144.120:443 and there is an api token `qqgfHAtBuja8liwcOafzXzm4WHcWYOb`.

To send an SMS you would use notify_smseagle like this:

```
notify_smseagle -u "https://192.168.144.120" -t "qqgfHAtBuja8liwcOafzXzm4WHcWYOb" -r "+49123456789" -m "nothingtoreadhere"
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
