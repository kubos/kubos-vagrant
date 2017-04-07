#!/usr/local/bin/python

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
    if args.all or args.upload:
        upload_box(args)


def main():
    parser = argparse.ArgumentParser(
        description='Provision and package the kubostech/base and/or kubostech/kubos-dev box and upload it to the Vagrant Cloud.')

    parser.add_argument('box_name',
                        nargs=1,
                        choices=['all', 'base', 'kubos-dev'],
                        help='Specify the vagrant box name')

    parser.add_argument('version',
                        nargs=1,
                        help='Specify the version of the upload.')


    resume_parser = parser.add_mutually_exclusive_group(required=False)
    resume_parser.add_argument('--feature', dest='resume', action='store_true')
    resume_parser.add_argument('--no-feature', dest='resume', action='store_false')
    parser.set_defaults(resume=True)


    parser.add_argument('-a', '--all',
                        action='store_true',
                        default=False,
                        help='Provision, Package and Upload the box to Vagrant Cloud.')

    parser.add_argument('-c', '--clean',
                        action='store_true',
                        default=False,
                        help='Delete any pre-existing build files for this version and rebuild from scratch.')

    parser.add_argument('--provision',
                        action='store_true',
                        default=False,
                        help='Only provision the box but do not package or upload it.')

    parser.add_argument('--provision-no-clone',
                        action='store_true',
                        default=False,
                        help='Provision the box without trying to reclone the repo.')

    parser.add_argument('--package',
                        action='store_true',
                        default=False,
                        help='Skip provisioning and uploading the box. Only package the box.')

    parser.add_argument('-u', '--upload',
                        action='store_true',
                        default=False,
                        help='Skip the provisioning and building steps. Only upload the box.')

    parser.add_argument('--upload-no-create-version',
                        action='store_true',
                        default=False,
                        help='Skip creating the version when uploading the box')

    parser.add_argument('--upload-no-create-provider',
                        action='store_true',
                        default=False,
                        help='Skip creating the provider when uploading the box')

    parser.add_argument('--upload-no-box-upload',
                        action='store_true',
                        default=False,
                        help='Skip the box upload step of the upload process')

    parser.add_argument('--upload-no-release',
                        action='store_true',
                        default=False,
                        help='Skip the release step after uploading the box')

    parser.add_argument('-b', '--box',
                        default=None,
                        help='Specify a non-default Vagrant box directory (points to a Vagrantfile or the directory containing the Vagrant file)')

    args, following_args = parser.parse_known_args()
    args.version = args.version[0] #version is initially a list of 1 element
    args.box_name = args.box_name[0]
    if args.box_name == 'all':
        args.box_name = 'base'
        build_box(args)
        args.box_name = 'kubos-dev'
        build_box(args)
    else:
        build_box(args)


if __name__ == '__main__':
    main()
