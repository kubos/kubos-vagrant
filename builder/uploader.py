'''
This is the upload script for packaging the final box package and uploading it to the Vagrant Cloud
'''

import argparse
import logging
import json
import os
import subprocess
import sys
import requests
from utils import BoxAutomator

def BoxUploader(BoxAutomator):
    CURL = 'curl'
    PROVIDER = 'virtualbox'
    USER_NAME = 'kubostech'
    BASE_URL = 'https://atlas.hashicorp.com/api/v1/box/%s/%s' % (self.USER_NAME, self.BOX_NAME)

    def __init__(self, version):
        super(BoxAutomator, self).init(version)
        ACCESS_TOKEN = os.environ['VAGRANT_CLOUD_ACCESS_TOKEN']

        if ACCESS_TOKEN is None:
            print >>sys.stderr, 'The VAGRANT_CLOUD_ACCESS_TOKEN environment variable needs to be set.'
            sys.exit(1)


    def check_http_response(res):
        if not res.ok:
            print >>sys.stderr, 'Something went wrong. Received a %i return code' % res.status_code
            print >>sys.stderr, res.content
            sys.exit(1)


    def create_version(self):
        print 'Attempting to create version %s' % self.version
        create_url = '%s/versions' % self.BASE_URL
        headers = {
                   'X-Atlas-Token': self.ACCESS_TOKEN
        }
        data = {
          'version[version]': self.version
        }
        res = requests.post(create_url, headers=headers, data=data)
        self.check_http_response(res)
        return res


    def create_provider(self):
        print 'Creating Provider...'
        create_url = '%s/version/%s/providers' % (self.BASE_URL, self.version)
        headers = {
                   'X-Atlas-Token': self.ACCESS_TOKEN
        }
        data = {
            'provider[name]': self.PROVIDER
        }
        res = requests.post(create_url, headers=headers, data=data)
        self.check__http_response(res)
        return res


    def get_upload_status(self):
        print 'Getting Upload Status...'
        status_url = '%s/version/%s/provider/virtualbox/upload?access_token=%s'\
                        % (self.BASE_URL, self.version, selfACCESS_TOKEN)
        res = requests.get(status_url)
        self.check_http_response(res)
        return res


    def submit_upload(self, path, upload_url):
        print 'Uploading box file %s' % path
        #The requests mulitpart file upload is being rejected by the Vagrant API - Just using a curl shell command for now
        # upload_file = {'file': open(path)}
        # res = requests.put(upload_url, files=upload_file)
        # return res

        upload_response = self.run_cmd(CURL, '-X', 'PUT', '--upload-file', path, upload_url)


    def release_version(self):
        print 'Releasing Version: %s' % self.version
        release_url = '%s/version/%s/release' % (self.BASE_URL, self.version)
        headers = {
                   'X-Atlas-Token': self.ACCESS_TOKEN
        }
        res = requests.put(release_url, headers=headers)
        self.check_http_response(res)
        return res


    def get_version_status(version):
        status_url = '%s/version/%s/provider/%s?access_token=%s' % (BASE_URL, version, PROVIDER, ACCESS_TOKEN)
        res = requests.get(status_url)
        check_http_response(res)
        return res


    def upload_box(args):
        '''
        The REST API upload workflow is:

        1) Create a new version of the box
        2) Create a virtualbox provider for the new version
        3) Get our upload endpoint and upload token
        4) Upload the *.box file
        5) Release the version
        6) Get the version status and make sure the hosted token matches our upload token from step 3
           to make sure the released box matches the same one we uploaded.
        '''

        success_key = 'success'
        errors_key  = 'errors'

        path = validate_path(path)

        if args.all or not args.upload_no_create_version:
            create_version_response = create_version(args.version)
        if args.all or not args.upload_no_create_provider:
            create_provider_response = create_provider(args.version)
        status_response = get_upload_status(args.version)
        status_data = status_response.json()

        if success_key in status_data:
            if not status_data[success_key]:
                print >>sys.stderr,'Errors: %s' % status_data[errors_key]
                sys.exit(1)
        upload_url   = status_data['upload_path']
        upload_token = status_data['token']

        submit_upload(path, upload_url)
        if args.all or not args.upload_no_release:
            release_response = release_version(args.version)
            verification_response = get_version_status(args.version)
            hosted_token = verification_response.json()['hosted_token']

            if upload_token == hosted_token:
                print 'Successfully uploaded and released box %s/%s version %s' % (USER_NAME, BOX_NAME, version)
            else:
                print >>sys.stderr, 'The upload and hosted tokens do not match - Something went wrong with the upload and release process'
                sys.exit(1)


    if __name__ == '__main__':
        main()

