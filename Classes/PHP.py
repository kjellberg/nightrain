__author__ = 'naetech'

import os
import subprocess
import re
import threading
import time
import sys

from threading import Thread

class PHP:

    def found(self, php_path):

        if not os.path.exists(php_path):
            return False

        # attempt to execute php by shell -v
        process_output = subprocess.check_output([php_path, "-v"])

        # check if the output contains zend anywhere
        if "Zend Engine" in process_output:
            return True
        else:
            return False

    def valid(self, php_path):
        process_output = subprocess.check_output([php_path, "-v"])
        matcher = re.compile("PHP 5.[0-9]+.[0-9]+")
        if matcher.match(process_output):
            return True
        else:
            return False

    def start_server(self, php_path, port, webroot):
        command = '{0} -S localhost:{1} -t {2}'.format(php_path, port, webroot)
        # os.system(command)
        subprocess.call(command, shell=True)

class PHPServerThread (threading.Thread):

    php_path = None
    port = None
    webroot = None

    def __init__(self, php_path, port, webroot):
        threading.Thread.__init__(self)
        self.php_path = php_path
        self.port = port
        self.webroot = webroot

    def run(self):
        php_executable = PHP()
        if php_executable.found(self.php_path):
            if php_executable.valid(self.php_path):
                php_executable.start_server(self.php_path, self.port, self.webroot)

    def stop(self):
        sys.exit()

    def pause_execution(self, seconds):
        time.sleep(seconds)