__author__ = 'naetech'

import os
import subprocess
import re
import threading
import signal

from threading import Thread

class PHP:

    program_php_server_thread = None

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

    def start_server_in_a_thread(self, php_path, port, webroot):
        self.program_php_server_thread = PHPServerThread(php_path, port, webroot)
        self.program_php_server_thread.start()

    def stop_server_in_a_thread(self):
        print "Trying to close the PHP process on %s" % (self.program_php_server_thread.php_server_process.pid)
        try:
            os.killpg(self.program_php_server_thread.php_server_process.pid, signal.SIGTERM)
        except:
            print "Something weird happened"

class PHPServerThread (threading.Thread):

    php_path = None
    port = None
    webroot = None
    php_executable = None
    php_server_process = None

    def __init__(self, php_path, port, webroot):
        threading.Thread.__init__(self)
        self.php_path = php_path
        self.port = port
        self.webroot = webroot

    def start_server(self):
        command = '{0} -S localhost:{1} -t {2}'.format(self.php_path, self.port, self.webroot)
        self.php_server_process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

    def run(self):
        self.start_server()