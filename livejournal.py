#!/usr/bin/python

import httplib
import urllib
import sys

class ProtocolException(RuntimeError):
    pass

class LJ(object):
    def __init__(self, username, password, usejournal=None):
        self.conn = None
        self.username = username
        self.password = password
        self.usejournal = usejournal

    def run(self, mode, **params):
        if not self.conn:
            self.conn = httplib.HTTPConnection('www.livejournal.com', 80)
            self.conn.connect()
        allparams = {
            'user': self.username,
            'password': self.password,
            'clientversion': 'goodbye',
            'ver': '1',
            'mode': mode
            }
        if self.usejournal:
            allparams['usejournal'] = self.usejournal
        allparams.update(params)
        self.conn.request('POST', '/interface/flat',
                          urllib.urlencode(allparams),
                          {'Content-Type':
                               'application/x-www-form-urlencoded'})
        resp = self.conn.getresponse()
        body = resp.read()
        if resp.status != 200:
            raise ProtocolException(body)
        lines = body.strip().split('\n')
        result = {}
        for i in range(0, len(lines), 2):
            result[lines[i]] = lines[i+1]
        if 'success' not in result or result['success'] != 'OK':
            raise ProtocolException(body)
        return result
