# netdata-needrestart

Check/graph the number of processes/services/kernels that should be restarted after upgrading packages.

![](https://i.imgur.com/ebD2MTW.png)

This is a `python.d` module for [netdata](https://my-netdata.io/).

When no restarts are required all charts will have a value of 0. Values higher than 0 indicate that a restart is required, or that there was an error opening/reading the log file. The chart is always visible when the module is installed.




## Installation

Install [`needrestart`](https://fiasko.io/tag/needrestart.html)

This module expects the last [batch](https://github.com/liske/needrestart/blob/master/README.batch.md) output of needrestart at `/var/log/needrestart.log`. Add a cron job to generate this file periodically, for example in `/etc/cron.d/needrestart`:

```
0,30 * * * * root /usr/sbin/needrestart -b > /var/log/needrestart.log 2>&1
```

Copy the required files and restart netdata:

```bash
git clone https://gitlab.com/nodiscc/netdata-needrestart
cp netdata-needrestart/needrestart.chart.py netdata-needrestart/needrestart.conf /opt/netdata/python.d/
systemctl restart netdata
```

You can get details on which services need to be restarted by reading mail sent by needrestart, running `needrestart`, or reading the log file.

You can schedule an automatic restart with `needrestart -r a`.

## Configuration

No configuration is required. Common `python.d` plugin options can be changed in [`needrestart.conf`](needrestart.conf).

The default `update every` value is 120 seconds so the initial chart will only be created after 2 minutes. Change this value if you need more accuracy.


## Debug

To debug this module:

```bash
$ sudo su -s /bin/bash netdata
$ /opt/netdata/usr/libexec/netdata/plugins.d/python.d.plugin 1  debug trace needrestart
```

## TODO

- Document alarm when status != 0 for more than `update every`
- Configure needrestart to generate the status file after each APT run (see `/etc/needrestart/notify.d/600-mail`)

## License

[GNU GPLv3](LICENSE)

[Github.com mirror](https://github.com/nodiscc/netdata-needrestart)
