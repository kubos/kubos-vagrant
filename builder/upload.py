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

'''
This is the upload script for packaging the final box package and uploading it to the Vagrant Cloud
'''

import json
import os
import requests
import subprocess
import sys

from utils import BoxAutomator

class BoxUploader(BoxAutomator):
    BOX_FILE_NAME = 'package.box' # This is the default name given from `vagrant package`
    BOX_NAME = 'kubos'
    CURL = 'curl'
    PROVIDER = 'virtualbox'
    USER_NAME = 'kubos'
    BASE_URL = 'https://atlas.hashicorp.com/api/v1/box/%s/%s' % (USER_NAME, BOX_NAME)
    STATUS_KEY = 'upload'

    status_steps = {
            'base':      ['create_version',
                          'create_provider',
                          'get_upload_status',
                          'submit_upload',
                          'release_version',
                          'verify_release'],
            'kubos-dev': ['create_version',
                          'create_provider',
                          'get_upload_status',
                          'submit_upload',
                          'release_version',
                          'verify_release']

                }


    def __init__(self, args):
        super(BoxUploader, self).__init__(args)
        self.BASE_URL = 'https://app.vagrantup.com/api/v1/box/%s/%s' % (self.USER_NAME, self.name)
        self.ACCESS_TOKEN = os.environ['VAGRANT_CLOUD_ACCESS_TOKEN']
        self.setup_status()

        if self.ACCESS_TOKEN is None:
            print('The VAGRANT_CLOUD_ACCESS_TOKEN environment variable needs to be set.')
            sys.exit(1)


    def check_http_response(self, res):
        if not res.ok:
            print('Something went wrong. Received a {} return code'.format(res.status_code), file=sys.stderr)
            print(res.content, file=sys.stderr)
            sys.exit(1)


    def create_version(self):
        if self.resume:
            if self.check_status('create_version'):
                print('Version previously created.. Skipping...')
        print('Attempting to create version {}'.format(self.version))
        create_url = '%s/versions' % self.BASE_URL
        headers = {
                   'X-Atlas-Token': self.ACCESS_TOKEN
        }
        data = {
          'version[version]': self.version
        }
        res = requests.post(create_url, headers=headers, data=data)
        self.check_http_response(res)
        self.update_status('create_version')
        return res


    def create_provider(self):
        if self.resume:
            if self.check_status('create_provider'):
                print('Provider previously created... Skipping...')
        print('Creating Provider...')
        create_url = '%s/version/%s/providers' % (self.BASE_URL, self.version)
        headers = {
                   'X-Atlas-Token': self.ACCESS_TOKEN
        }
        data = {
            'provider[name]': self.PROVIDER
        }
        res = requests.post(create_url, headers=headers, data=data)
        self.check_http_response(res)
        self.update_status('create_provider')
        return res


    def get_upload_status(self):
        print('Getting Upload Status...')
        status_url = '%s/version/%s/provider/virtualbox/upload?access_token=%s'\
                        % (self.BASE_URL, self.version, self.ACCESS_TOKEN)
        res = requests.get(status_url)
        self.check_http_response(res)
        self.update_status('get_upload_status')
        return res


    def submit_upload(self,  upload_url):
        if self.resume:
            if self.check_status('submit_upload'):
                print('Box previously uploaded... Skipping...')
        print('Uploading box file {}'.format(self.path))
        # The requests mulitpart file upload is being rejected by the Vagrant API - Just using a curl shell command for now
        # upload_file = {'file': open(path)}
        # res = requests.put(upload_url, files=upload_file)
        # return res
        upload_response = self.run_cmd(self.CURL, '-X', 'PUT', '--upload-file', self.box_path, upload_url)
        self.update_status('submit_upload')


    def release_version(self):
        if self.resume:
            if self.check_status('release_version'):
                print('Version previously released... Skipping...')
        print('Releasing Version: {}'.format(self.version))
        release_url = '%s/version/%s/release' % (self.BASE_URL, self.version)
        headers = {
                   'X-Atlas-Token': self.ACCESS_TOKEN
        }
        res = requests.put(release_url, headers=headers)
        self.check_http_response(res)
        self.update_status('release_version')
        return res


    def get_version_status(self):
        status_url = '%s/version/%s/provider/%s?access_token=%s' % (self.BASE_URL, self.version, self.PROVIDER, self.ACCESS_TOKEN)
        res = requests.get(status_url)
        self.check_http_response(res)
        return res


def upload_box(args):
    '''
    The REST API upload workflow is:

    1) Create a new version of the box
    2) Create a VirtualBox provider for the new version
    3) Get our upload endpoint and upload token
    4) Upload the *.box file
    5) Release the version
    6) Get the version status and make sure the hosted token matches our upload token from step 3
       to make sure the released box matches the same one we uploaded.
    '''
    uploader = BoxUploader(args)

    success_key = 'success'
    errors_key  = 'errors'

    uploader.validate_box_path(args)
    # Create the new version
    create_version_response = uploader.create_version()
    # Add the VirtualBox provider
    create_provider_response = uploader.create_provider()

    status_response = uploader.get_upload_status()
    status_data = status_response.json()

    if success_key in status_data:
        if not status_data[success_key]:
            print('Errors: {}'.format(status_data[errors_key]), file=sys.stderr)
            sys.exit(1)
    upload_url   = status_data['upload_path']
    upload_token = status_data['token']

    # Upload the box file
    uploader.submit_upload(upload_url)

    if not args.halt_release:
        release_response = uploader.release_version()
        verification_response = uploader.get_version_status()
        hosted_token = verification_response.json()['hosted_token']

        if upload_token == hosted_token:
            print('Successfully uploaded and released box {}/{} version {}'.format(uploader.USER_NAME, uploader.BOX_NAME, uploader.version))
            uploader.update_status('verify_release')
        else:
            print('The upload and hosted tokens do not match - Something went wrong with the upload and release process', file=sys.stderr)
            sys.exit(1)

