# Kubos SDK
# Copyright (C) 2017 Kubos Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import vagrant
from utils import BoxAutomator

class BoxPackager(BoxAutomator):

    def __init__(self, version):
        super(BoxPackager, self).__init__(version)


    def package(self, args):
        self.validate_path(args.box)

        print 'Starting Box Packaging Process...'
        v = vagrant.Vagrant()
        try:
            v.package()
            print 'Packaging completed successfully...'
        except subprocess.CalledProcessError as e:
            print>>sys.stderr, 'Error: The package step failed'
            sys.exit(1)


def package_box(args):
    packager = BoxPackager(args.version)
    packager.package(args)

