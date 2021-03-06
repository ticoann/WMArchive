#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable=
"""
File       : BaseIO.py
Author     : Valentin Kuznetsov <vkuznet AT gmail dot com>
Description: Base class to define storage APIs. It contains
             individual _read/_write methods for single record
             or bulk read/write methods for list of records.
             The subclasses can either implement _read/_write
             or read/write methods.
"""

# futures
from __future__ import print_function, division

# system modules
from types import GeneratorType

# WMArchive modules
from WMArchive.Utils.Utils import wmaHash
from WMArchive.Utils.Utils import tstamp

class Storage(object):
    "Base class which defines storage APIs"
    def __init__(self, uri=None):
        self.uri = uri
        self.empty_data = [] # we will always return a list

    def log(self, msg):
        "log API"
        print(tstamp('WMA %s' % self.__class__.__name__), msg)

    def _write(self, data):
        "Internal write API, should be implemented in subclasses"
        pass

    def write(self, data, safe=False):
        "Write API, return ids of stored documents"
        wmaids = self.getids(data)
        if  isinstance(data, list) or isinstance(data, GeneratorType):
            for rec in data:
                self.log('write %s' % rec['wmaid'])
                self._write(rec)
        elif isinstance(data, dict):
            self.log('write %s' % data['wmaid'])
            self._write(data)

        # if safe argument is provided we'll read data again and check it
        if  safe:
            if  isinstance(data, dict):
                data = [data]
            docs = self.read(wmaids)
            for rec1, rec2 in zip(data, docs):
                if rec1 != rec2:
                    raise Exception('Data mismatch: %s %s' % (rec1, rec2))
        return wmaids

    def _read(self, query=None):
        "Internal read API, should be implemented in subclasses"
        return self.empty_data

    def read(self, spec=None):
        "Read data from local storage for given spec"
        if  isinstance(spec, list):
            out = []
            for item in spec:
                res = self._read(item)
                if  res:
                    out.append(res)
            return out
        return self._read(spec)

    def update(self, ids, spec):
        "Update documents with given set of document ids and update spec"
        pass

    def getids(self, data):
        "Return list of wmaids for given data"
        if  isinstance(data, list) or isinstance(data, GeneratorType):
            return [r['wmaid'] for r in data]
        return data['wmaid']

    def check(self, data):
        "Cross-check the data based on its wmaid"
        try:
            wmaid = data.pop('wmaid')
        except:
            wmaid = ''
        hid = wmaHash(data)
        if  hid != wmaid:
            raise Exception("Invalid data hash, hid=%s, wmaid=%s, data=%s" \
                    % (hid, wmaid, data))
