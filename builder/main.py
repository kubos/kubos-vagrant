#!/usr/bin/env python3

# Copyright (C) 2019 Kubos Corporation
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

import argparse

from utils     import clean_build
from provision import provision_box
from package   import package_box
from upload    import upload_box

def build_box(args):
    if args.clean:
        clean(args)

    if args.all or args.provision:
        provision_box(args)
    if args.all or args.package:
        package_box(args)

def main():
    parser = argparse.ArgumentParser(
        description='Provision and package the kubos/kubos-dev box.')

    parser.add_argument('version',
                        nargs=1,
                        help='Specify the version of the box.')

    resume_parser = parser.add_mutually_exclusive_group(required=False)
    resume_parser.add_argument('--resume', dest='resume', action='store_true')
    resume_parser.add_argument('--no-resume', dest='resume', action='store_false')
    parser.set_defaults(resume=True)

    parser.add_argument('-a', '--all',
                        action='store_true',
                        default=False,
                        help='Provision and Package the box.')

    parser.add_argument('-l', '--local',
                        action='store_true',
                        default=False,
                        help='Run and build with the local repo, rather than cloning the kubos vagrant repo')

    parser.add_argument('-c', '--clean',
                        action='store_true',
                        default=False,
                        help='Delete any pre-existing build files for this version and rebuild from scratch.')

    parser.add_argument('--provision',
                        action='store_true',
                        default=False,
                        help='Only provision the box and exit')

    parser.add_argument('--package',
                        action='store_true',
                        default=False,
                        help='Package the box and exit. Skip provisioning and uploading the box.')

    parser.add_argument('-b', '--box',
                        default=None,
                        help='Specify a non-default Vagrant box directory (points to a Vagrantfile or the directory containing the Vagrant file)')

    args, following_args = parser.parse_known_args()
    args.version = args.version[0] # Version is initially a list of 1 element
    args.box_name = "kubos-dev"
    build_box(args)


if __name__ == '__main__':
    main()
