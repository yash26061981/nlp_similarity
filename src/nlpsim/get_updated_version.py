#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

import sys
from pathlib import Path  # path tricks so we can import wherever the module is
sys.path.append(os.path.abspath(Path(os.path.dirname(__file__)) / Path("../..")))
_sourcepath = os.path.abspath(Path(os.path.dirname(__file__)) / Path(''))

import fileinput
from nlpsim._version import __version__
from datetime import date, datetime

# Semantic Versioning
# Semantic versioning follows the pattern of X.Y.Z
# Or more readable would be [major].[minor].[build/release]
# E.g. 1.2.build


class VersionManager:
    def __init__(self):
        self.version_file = os.path.join(_sourcepath, '_version.py')
        # creating the date object of today's date
        self.todays_date = date.today()
        self.todays_date_str = self.todays_date.strftime("%Y.%m.%d")
        pass

    @staticmethod
    def split_version(current_version):
        return current_version.split('.')

    def get_version_str(self, current_version, index):
        return self.split_version(current_version)[index]

    def get_version_date(self, current_version):
        date_time_str = ".".join(s for s in self.split_version(current_version)[0:-1])
        date_time_obj = datetime.strptime(date_time_str, "%Y.%m.%d")
        return date_time_obj.date()

    def check_if_date_changed(self, current_version):
        version_date = self.get_version_date(current_version)
        if version_date < self.todays_date:
            return True
        return False

    def get_version(self):
        current_version = __version__
        patch = self.get_version_str(current_version, 3)
        patch = 1 if self.check_if_date_changed(current_version) else int(patch) + 1

        new_version = self.todays_date_str + '.' + str(patch)

        with fileinput.FileInput(self.version_file, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(current_version, new_version), end='')
        os.remove(self.version_file + '.bak')
        return new_version

    def get_version_major_minor(self, build=True):
        current_version = __version__
        major = int(self.get_version_str(current_version, 0))
        minor = int(self.get_version_str(current_version, 1))
        minor += 1
        if minor > 9:
            major += 1
            minor = 0
        if build:
            new_version = str(major) + '.' + str(minor)  # + '.0-build'
        else:
            new_version = str(major) + '.' + str(minor)  # + '.0-release'

        with fileinput.FileInput(self.version_file, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(current_version, new_version), end='')
        os.remove(self.version_file + '.bak')
        return new_version


if __name__ == '__main__':
    vm = VersionManager()
    nvm = vm.get_version()
    print(nvm)