import os
import time
import logging
import gevent
import emokit
from emokit.emotiv import Emotiv

from posdbos.source.dummy_data_source import DummyPacketSource


scriptPath = os.path.dirname(os.path.abspath(__file__))

emokit.emotiv.DEVICE_POLL_INTERVAL = 0.001

class EmotivConnector(object):

    def __init__(self, display_output=False, write=True, verbose=False, output_path=".", oldScript=False):
        self.oldScript = oldScript
        if self.oldScript:
            self._initOldEmotiv(display_output, write)
        else:
            self._initEmotiv(display_output, write, verbose, output_path)

    def _initEmotiv(self, display_output, write, verbose, output_path):
        self.emotiv = Emotiv(display_output=display_output, write=write, verbose=verbose, output_path=output_path)
        if not self._isEmotivConnected():
            self.close()
            self._loadDummyData()

    def _isEmotivConnected(self):
        return self.emotiv.running

    def _initOldEmotiv(self, display_output, write_to_file):
        self.emotiv = Emotiv(display_output, write_to_file)
        gevent.spawn(self.emotiv.setup)
        gevent.sleep(0)
        if not self._isOldEmotivConnected():
            self.emotiv.close()
            self._loadDummyData()

    def _isOldEmotivConnected(self):
        return self.emotiv.serial_number

    def _loadDummyData(self):
        filePath = scriptPath + "/../../../data/dummy_4096.csv"
        self.emotiv = DummyPacketSource(filePath)
        self.emotiv.convert()

    def dequeue(self):
        return self.emotiv.dequeue()

    def stop(self):
        try:
            if self.oldScript:
                self.emotiv.close()
            else:
                self.emotiv.stop()
        except Exception as e:
            logging.error(e.message)

    def close(self):
        self.stop()

if __name__ == "__main__":
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    output_path = scriptPath + "/../data/"

    headset = EmotivConnector(display_output=False, write=True, verbose=True, output_path=output_path)
    logging.info("Serial Number: %s" % headset.emotiv.serial_number)

    while headset.emotiv.running:
        try:
            packet = headset.dequeue()
        except Exception:
            headset.stop()
        time.sleep(0.0001)
    headset.stop()
