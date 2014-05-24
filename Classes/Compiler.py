__author__ = 'naetech'

import sys
import os
import shutil
from subprocess import call

class Compiler:

    build_dir = "./build"
    output_dir = "./dist"
    tmp_dir = "./nrtmp"
    resources_dir = "./resources"
    php_linux_binary_dir = "/home/naetech/php"

    def __init__(self, output_dir, tmp_dir, resources_dir):
        self.output_dir = output_dir
        self.tmp_dir = tmp_dir
        self.resources_dir = resources_dir

    def isLinux(self):

        platform = sys.platform
        if "linux" in platform:
            return True
        else:
            return False

    # todo check for windows
    def isWindows(self):
        pass

    # todo check for mac
    def isMac(self):
        pass

    # todo compile php for windows
    def compilePHPWindows(self):
        pass

    # todo compile php for mac
    def compilePHPMac(self):
        pass

    def compilePHPLinux(self):

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

        configureCommand = "cd %s && ./configure --prefix=%s" % (phpSourceDir, self.php_linux_binary_dir)
        call(configureCommand, shell=True)

        makeCommand = "cd %s && make && make install" % (phpSourceDir)
        call(makeCommand, shell=True)

        return True

    # todo compile nr for windows
    def compileNightrainWindows(self):
        pass

    # todo compile nr for linux
    def compileNightrainLinux(self):
        self.cleanUnncessaryFiles()
        spec_path = "--specpath=%s/%s" % (self.build_dir, "specs")
        call(["pyinstaller", "--clean", "-y", "-F", spec_path, "-n", "nightrain", "Application.py"])
        self.cleanUnncessaryFiles()

    # todo compile nr for mac
    def compileNightrainMac(self):
        pass

    def copyResources(self):

        items = [
            "php.ini",
            "www",
            "settings.ini",
            "icon.png",
            "LICENSE"
        ]

        for item in items:
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

    #todo copy php windows
    def copyPHPWindows(self):
        pass

    #todo copy php mac
    def copyPHPMac(self):
        pass

    def copyPHPLinux(self):
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

    def cleanDist(self):

        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def cleanUnncessaryFiles(self):

        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)