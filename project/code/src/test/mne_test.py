#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 19.09.2016

:author: Paul Pasler
:organization: Reutlingen University
'''

import sys, os
import unittest

import mne
import numpy as np

from config.config import ConfigProvider
from util.eeg_table_util import EEGTableFileUtil, EEGTableDto
from util.mne_util import MNEUtil
from numpy import array_equal
from numpy.testing.utils import assert_array_equal


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

PATH = os.path.dirname(os.path.abspath(__file__)) +  "/../../examples/"

def readData():
    return EEGTableFileUtil().readFile(PATH + "example_1024.csv")


class MNEUtilTest(unittest.TestCase):

    def setUp(self):
        self.mne = MNEUtil()
        self.config = ConfigProvider().getEmotivConfig()
        self.eegData = readData()

    def test_createInfo(self):
        channels = self.config.get("eegFields")
        samplingRate = self.config.get("samplingRate")

        info = self.mne._createInfo(channels, "testFile")
        self.assertEquals(info["sfreq"], samplingRate)
        self.assertEquals(info["nchan"], len(channels))
        self.assertItemsEqual(info["ch_names"], channels)

    def test_rawCreation(self):
        self.mne.createMNEObjectFromDto(self.eegData)

    def test_convertMNEToEEGTableDto(self):
        mneObj = self.mne.createMNEObjectFromDto(self.eegData)
        eegData2 = self.mne.convertMNEToEEGTableDto(mneObj)
        self.assertListEqual(self.eegData.getEEGHeader(), eegData2.getHeader())
        array_equal(self.eegData.getEEGData(), eegData2.getData())
        self.assertEqual(self.eegData.filePath, eegData2.filePath)

    def test_getChannels(self):
        channels = ["AF3", "F3"]
        raw = self.mne.createMNEObjectFromDto(self.eegData)
        chanObj = self.mne.getChannels(raw, channels)
        self.assertEqual(chanObj.info["nchan"], len(channels))

    def test_createMNEEpochsObject(self):
        epochs = self.mne.createMNEEpochsObject(self.eegData, 1)
        self.assertEqual(len(epochs.get_data()), 15)

    def createTestData(self):
        header = ["F3", "F4", "AF3", "AF4"]
        data = np.random.rand(4,512)
        filePath = "test"
        return self.mne.createMNEObject(data, header, filePath)

    def test__createEventsArray_overlapping(self):
        raw = self.createTestData()
        event_id = dict(drowsy=1)
        events1 = self.mne._createEventsArray(raw, 1, False)
        epochs1 = mne.Epochs(raw, events=events1, event_id=event_id, tmin=0.0, tmax=0.99, add_eeg_ref=True)
        
        events2 = self.mne._createEventsArray(raw, 1)
        epochs2 = mne.Epochs(raw, events=events2, event_id=event_id, tmin=0.0, tmax=0.99, add_eeg_ref=True)

        for i in range(0, len(events1)):
            data1 = epochs1[i].get_data()
            data2 = epochs2[i*2].get_data()
            self.assertTrue((data1 == data2).all())

    @unittest.skip("todo")
    def test_ICA(self):
        raw = self.mne.createMNEObjectFromDto(self.eegData)
        print self.mne.ICA(raw)

def testRawObject():
    # http://martinos.org/mne/stable/auto_tutorials/plot_creating_data_structures.html#creating-raw-objects
    # Generate some random data
    data = np.random.randn(5, 1000)
    # Initialize an info structure
    info = mne.create_info(
        ch_names=['MEG1', 'MEG2', 'EEG1', 'EEG2', 'EOG'],
        ch_types=['grad', 'grad', 'eeg', 'eeg', 'eog'],
        sfreq=100
    )
    
    custom_raw = mne.io.RawArray(data, info)
    print custom_raw

if __name__ == '__main__':
    unittest.main()