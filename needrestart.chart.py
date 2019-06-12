# -*- coding: utf-8 -*-
# Description: needrestart python.d module for netdata
# Author: nodiscc (nodiscc@gmail.com)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re

from bases.FrameworkServices.SimpleService import SimpleService

priority = 90000
update_every = 120

ORDER = [
    'status'
]

CHARTS = {
    'status': {
        'options': [None, 'Restart required', 'needs restart', 'status', 'needrestart.status', 'stacked'],
        'lines': [
            ['error', None, 'absolute'],
            ['kernel', None, 'absolute'],
            ['services', None, 'absolute'],
        ]
    }
}

RE_KERNEL = re.compile(r'NEEDRESTART-KSTA: [0|2|3]')
RE_SERVICES = re.compile(r'NEEDRESTART-SVC.*')

class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS

        self.data = dict()
        self.path = '/var/log/needrestart.log'
        self.modtime = ''
        self.data['error'] = 0
        self.data['kernel'] = 0
        self.data['services'] = 0

    def check(self):
        return True

    def get_data(self):
        if not is_readable(self.path) or is_empty(self.path):
            self.debug("{0} is unreadable or empty".format(self.path))
            self.data['error'] = 1
            self.data['kernel'] = 0
            self.data['services'] = 0
            return self.data
        else:
            self.data['error'] = 0

        try:
            if not self.is_changed():
                self.debug("{0} modification time is unchanged, returning previous values".format(self.path))
                return self.data
            file = open(self.path, 'r')
        except:
            self.error("Error while opening {0}".format(self.path))
            self.data['error'] = 1
            self.data['kernel'] = 0
            self.data['services'] = 0
            return self.data

        self.modtime = os.path.getmtime(self.path)
        lines = file.read()
        self.data['kernel'] = len(re.findall(RE_KERNEL, lines))
        self.data['services'] = len(re.findall(RE_SERVICES, lines))
        return self.data

    def is_changed(self):
        return self.modtime != os.path.getmtime(self.path)

def is_readable(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)

def is_empty(path):
    return os.path.getsize(path) == 0

