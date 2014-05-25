from Classes.Compiler import Compiler
from Classes.Settings import Settings

settings = Settings()
compiler = Compiler("./dist", "./nrtmp", "./Resources")

# clean output folder
compiler.clean_dist()

# compile nightrain

if compiler.is_windows():
    compiler.compile_nightrain_windows()

if compiler.is_linux():
    compiler.compile_nightrain_linux()

if compiler.is_mac():
    compiler.compile_nightrain_mac()

# compile PHP

if compiler.is_windows():
    compiler.compile_php_windows()

if compiler.is_linux():
    compiler.compile_php_linux()

if compiler.is_mac():
    compiler.compile_php_mac()

# copy required files
compiler.copy_resources()

if compiler.is_windows():
    compiler.copy_php_windows()

if compiler.is_linux():
    compiler.copy_php_linux()
    compiler.copy_php_ini_linux()

if compiler.is_mac():
    compiler.copy_php_mac()

settings.create_default_settings(compiler.get_settings_ini_dest())