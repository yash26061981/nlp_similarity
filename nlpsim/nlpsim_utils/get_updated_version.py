#!/usr/bin/python
import os
import sys
from pathlib import Path  # path tricks so we can import wherever the module is

sys.path.append(os.path.abspath(Path(os.path.dirname(__file__)) / Path("..")))
sys.path.append(os.path.abspath(Path(os.path.dirname(__file__)) / Path("../..")))

import fileinput
from nlpsim._version import __version__

# Semantic Versioning
# Semantic versioning follows the pattern of X.Y.Z
# Or more readable would be [major].[minor].[build/release]
# E.g. 1.2.build
version_file = 'nlpsim/_version.py'


class VersionManager:
    def __init__(self):
        pass

    @staticmethod
    def split_version(current_version):
        return current_version.split('.')

    def get_minor_version(self, current_version):
        return self.split_version(current_version)[1]

    def get_major_version(self, current_version):
        return self.split_version(current_version)[0]

    def get_build_release_version(self, current_version):
        patch = self.split_version(current_version)[2]
        return patch

    def get_version(self, build=True):
        current_version = __version__
        major = int(self.get_major_version(current_version))
        minor = int(self.get_minor_version(current_version))
        minor += 1
        if minor > 9:
            major += 1
            minor = 0
        if build:
            new_version = str(major) + '.' + str(minor) + '.build'
        else:
            new_version = str(major) + '.' + str(minor) + '.release'

        with fileinput.FileInput(version_file, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(current_version, new_version), end='')
        os.remove(version_file + '.bak')
        return new_version


if __name__ == '__main__':
    vm = VersionManager()
    nvm = vm.get_version()
    print(nvm)