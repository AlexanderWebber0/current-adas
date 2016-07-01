#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 05.04.2016

:author: Paul Pasler
:organization: Reutlingen University
'''

from copy import deepcopy

from numpy import hamming

from signal_window import SignalWindow


class HammingSignalWindow(SignalWindow):
    '''
    Implementation for hamming window function
    '''
    
    def __init__(self, windowSize, fields):
        super(HammingSignalWindow, self).__init__(windowSize)
        self.windowFunction = hamming(windowSize)
        self._initWindow(fields)
        self._resetWindow()
            
    def notifyObserver(self, data):
        data = self._doWindowFunction(data)
        for observer in self.observer:
            observer.notify(data)
    
    def _doWindowFunction(self, data):
        '''Simple window rectangular function '''
        #TODO hamming function must be applied to data["key"].value
        return data
    
    def _resetWindow(self):
        self.index = 0
        self.window = deepcopy(self.initWindow)

    def _initWindow(self, fields):
        self.initWindow = {}
        for key in fields:
            self.initWindow[key] = {"value": [], "quality": []}
    
    def _addDataToWindow(self, data):   
        for key, date in data.iteritems():
            field = self.window[key]
            field["value"].append(date["value"])
            field["quality"].append(date["quality"])
            
    def addData(self, data):
        #TODO potential bottleneck
        self._addDataToWindow(data)
        self.index += 1
        
        if self.isFull():
            data = self.window.copy()
            self._resetWindow()
            self.notifyObserver(data)
            
