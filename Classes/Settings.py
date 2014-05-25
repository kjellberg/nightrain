__author__ = 'naetech'

import Compiler

from tempfile import mkstemp
from shutil import move
from os import remove, close

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

    def create_default_settings(self, destination):
        config = ConfigParser.RawConfigParser(allow_no_value=True)

        config.add_section("Application")

        config.set("Application", "; full path or the relative path to the PHP executable")
        if Compiler.Compiler.is_linux() or Compiler.Compiler.is_mac():
            config.set("Application", "php_path", "./lib/php/bin/php")
        else:
            config.set("Application", "php_path", "lib\\php\\php.exe")

        config.set("Application", "; full path or the relative path to the directory from where")
        if Compiler.Compiler.is_linux() or Compiler.Compiler.is_mac():
            config.set("Application", "webroot", "./www")
        else:
            config.set("Application", "webroot", "www")

        config.set("Application", "; default port from where PHP Nightrain launches its web server")
        config.set("Application", "; make sure your firewall is not blocking this port")
        config.set("Application", "port", "8000")

        config.set("Application", "; default application width")
        config.set("Application", "width", "800")

        config.set("Application", "; default application height")
        config.set("Application", "height", "600")

        config.set("Application", "; default window status (true or false)")
        config.set("Application", "maximized", False)

        config.set("Application", "; full screen (true or false)")
        config.set("Application", "; you can press 'F11' to toggle full screen as well while")
        config.set("Application", "; the application is running")
        config.set("Application", "fullscreen", False)

        config.set("Application", "; amount of time to wait before showing the application GUI")
        config.set("Application", "; this is useful if there is a delay in launching the web server")
        config.set("Application", "; or the firewall on your computer is interfering")
        config.set("Application", "wait_time", 0)

        with open(destination, 'wb') as config_file:
            config.write(config_file)

    @staticmethod
    def replace(file_path, pattern, subst):
        #Create temp file
        fh, abs_path = mkstemp()
        new_file = open(abs_path,'w')
        old_file = open(file_path)
        for line in old_file:
            new_file.write(line.replace(pattern, subst))
        #close temp file
        new_file.close()
        close(fh)
        old_file.close()
        #Remove original file
        remove(file_path)
        #Move new file
        move(abs_path, file_path)