# check_smseagle

## About

check_smseagle checks the GSM signal strength
of an [SMSEagle](http://www.smseagle.eu/) device.

## Requirements

Python 2.6 or 2.7 with SSL support

## Example

Let's say your device listens at 192.168.144.120:80 and there is
a login "jdoe" with the password "123456".
To monitor the GSM signal strength you would use the plugin like this:

```
check_smseagle -u http://192.168.144.120 -U jdoe -P 123456
```

You can increase the warning and critical thresholds
by adding the following options:

```
-w 20 -c 10
```

# notify_smseagle

## About

notify_smseagle sends SMS via an [SMSEagle](http://www.smseagle.eu/) device.

## Requirements

Python 2.6 or 2.7 with SSL support

## Example

Let's say your device listens at 192.168.144.120:80 and there is
a login "jdoe" with the password "123456".
To send an SMS you would use notify_smseagle like this:

```
notify_smseagle -u http://192.168.144.120 -U jdoe -P 123456 -t +49123456789 -m nothingtoreadhere
```

# smseagle_ack.cgi

## About

smseagle_ack.cgi is a CGI 1.1 script for the "callback url" function
of an [SMSEagle](http://www.smseagle.eu/) device.
It parses incoming SMSs and acknowledges host/service problems
if an SMS requests that.

## Requirements

Python 2.6 or 2.7

## Configuration

The script reads its configuration from the file specified in the
X_SMSEAGLE_ACK_CGI_CFG environment variable. Default: /etc/smseagle-ack-cgi.conf

### Example

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
