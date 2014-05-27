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

if compiler.is_windows():
    compiler.copy_resources()
    compiler.copy_php_windows()
    settings.create_default_settings(compiler.get_settings_ini_dest())

if compiler.is_linux():
    compiler.copy_resources()
    compiler.copy_php_linux()
    compiler.copy_php_ini_linux()
    settings.create_default_settings(compiler.get_settings_ini_dest())

if compiler.is_mac():
    app_version_dir = "%s/%s" % (compiler.output_dir, "app_version")
    shell_version_dir = "%s/%s" % (compiler.output_dir, "shell_version")

    nightrain_app_file_dest = "%s/nightrain.app" % app_version_dir
    nightrain_shell_file_dest = "%s/nightrain" % shell_version_dir

    nightrain_app_file_source = "%s/nightrain.app" % compiler.output_dir
    nightrain_shell_file_source = "%s/nightrain" % compiler.output_dir

    # create the output directories
    compiler.make_dir(app_version_dir)
    compiler.make_dir(shell_version_dir)

    # move nightrain.app to app version dir
    compiler.move_file(nightrain_app_file_source, nightrain_app_file_dest)

    # move nightrain shell version to shell version dir
    compiler.move_file(nightrain_shell_file_source, nightrain_shell_file_dest)

    # copy PHP libraries to app version
    destination = "%s/Contents/MacOS/lib/php" % nightrain_app_file_dest
    compiler.copy_php_mac(destination)

    # copy PHP libraries to shell version
    destination = "%s/lib/php" % shell_version_dir
    compiler.copy_php_mac(destination)

    # copy resources to app version
    mac_os_x_dir = "%s/Contents/MacOS" % nightrain_app_file_dest
    compiler.copy_resources(mac_os_x_dir)
    settings.create_default_settings("%s/%s" % (mac_os_x_dir, "settings.ini"))

    # copy resources to shell version
    compiler.copy_resources(shell_version_dir)
    settings.create_default_settings("%s/%s" % (shell_version_dir, "settings.ini"))

    # copy PHP ini to app version
    destination = "%s/Contents/MacOS/lib/php/bin/php.ini" % nightrain_app_file_dest
    compiler.copy_php_ini_mac(destination)

    # copy php ini to app version
    destination = "%s/lib/php/bin/php.ini" % shell_version_dir
    compiler.copy_php_ini_mac(destination)