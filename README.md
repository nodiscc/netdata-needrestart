# netdata-needrestart

Check/graph the number of processes/services/kernels that should be restarted after upgrading packages.

![](https://i.imgur.com/ebD2MTW.png)

This is a `python.d` module for [netdata](https://my-netdata.io/). It parses output from [needrestart](https://fiasko.io/tag/needrestart.html).

When no restarts are required all charts will have a value of 0. Values higher than 0 indicate that a restart is required, or that there was an error opening/reading the log file. The chart is always visible when the module is installed. Any value higher than 0 will raise a warning in netdata alarms (and trigger a notification).


## Installation

This module expects the last [batch](https://github.com/liske/needrestart/blob/master/README.batch.md) output of needrestart at `/var/log/needrestart.log`


```bash
# install needrestart
apt install needrestart

# clone the repository
git clone https://gitlab.com/nodiscc/netdata-needrestart

# generate the initial file
needrestart -b > /var/log/needrestart.log

# configure dpkg to refresh the file after each run
cp netdata-needrestart/etc_apt_apt.conf.d_99needrestart /etc/apt/apt.conf.d/99needrestart

# add a cron job to refresh the file every 30 minutes
cp netdata-needrestart/etc_cron.d_needrestart /etc/cron.d/needrestart

# install configuration files/alarms
cp netdata-needrestart/needrestart.chart.py /opt/netdata/python.d/
cp netdata-needrestart/needrestart.conf /opt/netdata/python.d/
cp netdata-needrestart/health.d_needrestart.conf /opt/netdata/etc/health.d/needrestart.conf

# restart netdata
systemctl restart netdata

```


## Configuration

No configuration is required. Common `python.d` plugin options can be changed in [`needrestart.conf`](needrestart.conf).

The default `update every` value is 120 seconds so the initial chart will only be created after 2 minutes. Change this value if you need more accuracy.

You can get details on which services need to be restarted by reading mail sent by needrestart, running `needrestart`, or reading the log file.

You can schedule an automatic restart at a convenient time, for example using `echo reboot | at 22:00`.


## Debug

To debug this module:

```bash
$ sudo su -s /bin/bash netdata
$ /opt/netdata/usr/libexec/netdata/plugins.d/python.d.plugin 1  debug trace needrestart
```

## TODO

- Graph one line for each service/kernel, by name

## License

[GNU GPLv3](LICENSE)

## Mirrors

- https://github.com/nodiscc/netdata-needrestart
- https://gitlab.com/nodiscc/netdata-needrestart

