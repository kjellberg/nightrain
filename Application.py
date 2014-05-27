__author__ = 'naetech'

import os
import module_locator

program_path = module_locator.module_path()

print "Program path is: %s" % program_path

from Classes.Settings import Settings
from Classes.PHP import PHP
from Classes.GUI import GUI

program_settings = Settings()

settings_file_path = "%s/%s" % (program_path, "settings.ini")

program_settings.load_settings(settings_file_path)

php_path = str(program_settings.read_setting("php_path"))

if not os.path.exists(php_path):
    # perhaps we should try something relative
    php_path = "%s/%s" % (program_path, php_path)

port = str(program_settings.read_setting("port"))

webroot = str(program_settings.read_setting("webroot"))

if not os.path.exists(webroot):
    # perhaps we should try something relative
    webroot = "%s/%s" % (program_path, webroot)

wait_time = int(program_settings.read_setting("wait_time"))
if str(program_settings.read_setting("maximized")) == "true":
    maximized = True
else:
    maximized = False
if str(program_settings.read_setting("fullscreen")) == "true":
    fullscreen = True
else:
    fullscreen = False
width = int(program_settings.read_setting("width"))
height = int(program_settings.read_setting("height"))

program_php = PHP()
program_gui = GUI()

if program_php.found(php_path):
    if program_php.valid(php_path):
        program_php.start_server_in_a_thread(php_path, port, webroot)
        if wait_time:
            print "Going to delay the execution by %s seconds" % wait_time
            program_settings.pause_execution(wait_time)
        program_gui.show_browser(maximized, fullscreen, width, height, port)
        program_php.stop_server_in_a_thread()
    else:
        program_gui.show_error("PHP Version is Invalid", "This Version of PHP is Not Supported")
else:
    program_gui.show_error("PHP Path is Invalid", "System could not find PHP at the specified path: %s "
                                                  "<br><br>Current Working Directory: %s"
                                                  "<br><br>Script Location: %s"
                          % (php_path, os.getcwd(), program_path))