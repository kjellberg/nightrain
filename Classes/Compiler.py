__author__ = 'naetech'

import sys
import os
import shutil
import urllib
import zipfile
import Settings

from subprocess import call

class Compiler:

    build_dir = "./build"
    output_dir = "./dist"
    tmp_dir = "./nrtmp"
    resources_dir = "./resources"
    php_linux_binary_dir = "/home/naetech/php"
    php_windows_binary_dir = "C:\\nightrain_php"

    def __init__(self, output_dir, tmp_dir, resources_dir):
        self.output_dir = output_dir
        self.tmp_dir = tmp_dir
        self.resources_dir = resources_dir

    @staticmethod
    def is_linux():

        platform = sys.platform
        if "linux" in platform:
            return True
        else:
            return False

    @staticmethod
    def is_windows():
        if "win" in sys.platform:
            return True
        else:
            return False

    # todo check for mac
    @staticmethod
    def is_mac():
        pass

    # todo compile php for windows
    def compile_php_windows(self):
        # remove the old binary
        if os.path.exists(self.php_windows_binary_dir):
            shutil.rmtree(self.php_windows_binary_dir)

        # create a random tmp directory
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

        os.mkdir(self.tmp_dir)

        # download the latest version of PHP
        php_file_zip_download_link = "http://windows.php.net/downloads/releases/php-5.5.12-nts-Win32-VC11-x86.zip"
        php_file_zip_dest = "%s/%s" % (self.tmp_dir, "php-5.5.12-Win32-VC11-x86.zip")
        print "Downloading %s" % php_file_zip_download_link
        urllib.urlretrieve(php_file_zip_download_link, php_file_zip_dest)
        print "Finished downloading %s" % php_file_zip_download_link

        zfile = zipfile.ZipFile(php_file_zip_dest)
        for name in zfile.namelist():
            (dirname, filename) = os.path.split(name)
            extracted_dir = "%s\\%s" % (self.php_windows_binary_dir, dirname)
            print "Decompressing " + filename + " on " + dirname
            if not os.path.exists(extracted_dir):
                os.makedirs(extracted_dir)
            zfile.extract(name, extracted_dir)

        return True

    # todo compile php for mac
    def compile_php_mac(self):
        pass

    def compile_php_linux(self):

        # remove the old binary
        if os.path.exists(self.php_linux_binary_dir):
            shutil.rmtree(self.php_linux_binary_dir)

        # create a random tmp directory
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

        os.mkdir(self.tmp_dir)

        # download the latest version of PHP
        phpTarFile = "%s/%s" % (self.tmp_dir, "php5512.tar.gz")
        call(["wget", "http://us1.php.net/get/php-5.5.12.tar.gz/from/this/mirror", "-O", phpTarFile])

        phpDir = "%s/%s" % (self.tmp_dir, "php5512")
        os.mkdir(phpDir)
        call(["tar", "-C", phpDir, "-zxvf", phpTarFile])

        # compile PHP
        phpSourceDir = "%s/%s" % (phpDir, "php-5.5.12")

        configureCommand = "cd %s && ./configure --prefix=%s " \
                           "--enable-bcmath " \
                           "--enable-calendar " \
                           "--enable-mbstring " \
                           "--with-curl " \
                           "--with-gd " \
                           "--with-mcrypt " \
                           "--with-mysql " \
                           "--with-pdo-mysql " \
                           "--with-sqlite3" \
                           % (phpSourceDir, self.php_linux_binary_dir)
        call(configureCommand, shell=True)

        makeCommand = "cd %s && make && make install" % (phpSourceDir)
        call(makeCommand, shell=True)

        return True

    def compile_nightrain_windows(self):
        self.clean_unncessary_files()
        spec_path = "--specpath=%s/%s" % (self.build_dir, "specs")
        application_icon = "--icon=%s/%s" % (self.resources_dir, "icon.ico")
        # fixme When using the -w option, the final executable causes error
        call(["pyinstaller", "--clean", "-y", "-F", spec_path, application_icon, "-n", "nightrain", "Application.py"])
        self.clean_unncessary_files()

    def compile_nightrain_linux(self):
        self.clean_unncessary_files()
        spec_path = "--specpath=%s/%s" % (self.build_dir, "specs")
        call(["pyinstaller", "--clean", "-y", "-F", spec_path, "-n", "nightrain", "Application.py"])
        self.clean_unncessary_files()

    # todo compile nr for mac
    def compile_nightrain_mac(self):
        pass

    def copy_resources(self):

        items = [
            "www",
            "icon.png",
            "LICENSE"
        ]

        for item in items:
            if item == "icon.png" and self.is_windows():
                continue

            source = "%s/%s" % (self.resources_dir, item)
            destination = "%s/%s" % (self.output_dir, item)
            if os.path.exists(source):
                error = "Could not copy item %s" % (item)
                success = "Successfully copied %s to %s" % (source, destination)
                if os.path.isfile(source):
                    try:
                        shutil.copyfile(source, destination)
                        print success
                    except:
                        print error
                        return False
                else:
                    try:
                        shutil.copytree(source, destination)
                        print success
                    except:
                        print error
                        return False
            else:
                print "%s does not exist" % (item)
                return False

    def copy_php_windows(self):
        print self.php_windows_binary_dir
        destination = "%s/%s/%s" % (self.output_dir, "lib", "php")
        if os.path.exists(self.php_windows_binary_dir):
            try:
                shutil.copytree(self.php_windows_binary_dir, destination)
                print "Successfully copied %s to %s" % (self.php_windows_binary_dir, destination)
                return True
            except:
                print "Could not copy %s to %s" % (self.php_windows_binary_dir, destination)
                return False
        else:
            return False

    #todo copy php mac
    def copy_php_mac(self):
        pass

    def copy_php_linux(self):
        destination = "%s/%s/%s" % (self.output_dir, "lib", "php")
        if os.path.exists(self.php_linux_binary_dir):
            try:
                shutil.copytree(self.php_linux_binary_dir, destination)
                print "Successfully copied %s to %s" % (self.php_linux_binary_dir, destination)
                return True
            except:
                print "Could not copy %s to %s" % (self.php_linux_binary_dir, destination)
                return False
        else:
            return False

    def copy_php_ini_linux(self):
        src = "%s/%s" % (self.resources_dir, "php.ini")
        destination = self.get_php_ini_dest()
        try:
            shutil.copyfile(src, destination)
            print "Successfully copied %s to %s" % (src, destination)
            return True
        except:
            return False

    def copy_php_ini_windows(self):
        php_ini_src = "%s\\%s" % (self.php_windows_binary_dir, "php.ini-production")
        php_ini_dest = self.get_php_ini_dest()
        if os.path.exists(php_ini_src):
            try:
                shutil.copyfile(php_ini_src, php_ini_dest)
                print "Successfully copied %s to %s" % (php_ini_src, php_ini_dest)

                # replace configs
                php_ini_configs = [
                    '; extension_dir = "ext"',
                    ';extension=php_gd2.dll',
                    ';extension=php_mbstring.dll',
                    ';extension=php_sqlite3.dll'
                ]

                for config in php_ini_configs:
                    config_uncommented = config.replace(";", "").strip()
                    Settings.Settings.replace(php_ini_dest, config, config_uncommented)
                    print "Replaced %s with %s in %s" % (config, config_uncommented, php_ini_dest)
                return True
            except:
                return False
        else:
            print "Could not find %s" % php_ini_src

    # todo copy php ini mac
    def copy_php_ini_mac(self):
        pass

    def clean_dist(self):

        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def clean_unncessary_files(self):

        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

    def get_php_ini_dest(self):
        if self.is_linux() or self.is_mac():
            return "%s/%s/%s/%s/%s" % (self.output_dir, "lib", "php", "bin", "php.ini")
        elif self.is_windows():
            return "%s/%s/%s/%s" % (self.output_dir, "lib", "php", "php.ini")
        else:
            return False

    def get_settings_ini_dest(self):
        return "%s/%s" % (self.output_dir, "settings.ini")