__author__ = 'naetech'

import ConfigParser
import time

class Settings:

    # an array to hold all the settings
    myConfig = None

    def load_settings(self, file):
        # if file found, populate the settings array and return true
        config = ConfigParser.RawConfigParser()
        if not config.read(file):
            return False
        else:
            self.myConfig = config

    def read_setting(self, key):
        # if array has key return value
        if not self.myConfig:
            return False
        else:
            value = self.myConfig.get("Application", key)
            print "Value for %s is %s" % (key, value)
            if not value:
                return False
            else:
                return value

    def pause_execution(self, seconds):
        time.sleep(seconds)