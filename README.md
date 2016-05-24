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
