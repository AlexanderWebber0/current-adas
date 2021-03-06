#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 19.12.2016

:author: Paul Pasler
:organization: Reutlingen University
'''

from datetime import datetime

class DateConverter(object):

    def __init__(self, datePattern, hourOffset=0):
        self.epoch = datetime(1970,1,1, hour=hourOffset)
        self.datePattern = datePattern

    def setPattern(self, datePattern):
        self.datePattern = datePattern

    def _appendMillis(self, dateString):
        if '.' not in dateString:
            return dateString + '.0'
        return dateString

    def matchesDatePattern(self, dateString):
        dateString = self._appendMillis(dateString)
        try:
            self.convertDate(dateString)
            return True
        except Exception:
            return False

    def convertDate(self, dateString):
        if dateString == "":
            return ""
        dateString = self._appendMillis(dateString)
        return self._toTimestamp(datetime.strptime(dateString, self.datePattern))
    
    # http://stackoverflow.com/questions/8777753/converting-datetime-date-to-utc-timestamp-in-python
    def _toTimestamp(self, date):
        timestamp = date - self.epoch
        return timestamp.total_seconds()