'''
This is the upload script for packaing the final box package and uploading it to the Vagrant Cloud
'''

import argparse
import logging
import json
import os
import subprocess
import sys
import requests

ACCESS_TOKEN = os.environ['VAGRANT_CLOUD_ACCESS_TOKEN']

if ACCESS_TOKEN is None:
    print >>sys.stderr, 'The VAGRANT_CLOUD_ACCESS_TOKEN environment variable needs to be set.'
    sys.exit(1)

BOX_NAME = 'kubos'
BOX_FILE_NAME = 'package.box' # This is the default name given from `vagrant package`
CURL = 'curl'
PROVIDER = 'virtualbox'
USER_NAME = 'kubostech'
VAGRANT_FILE  = 'Vagrantfile'

BASE_URL = 'https://atlas.hashicorp.com/api/v1/box/%s/%s' % (USER_NAME, BOX_NAME)

def run_cmd(*args, **kwargs):
    cwd = kwargs.get('cwd', os.getcwd())

    print ' '.join(args)

    try:
        return subprocess.check_output(args, **kwargs)
    except subprocess.CalledProcessError, e:
        print >>sys.stderr, 'Error executing command, giving up'
        sys.exit(1)


def validate_path(path):
    if not path:
        print 'path was not provided using default path..'
        path = os.path.join(os.getcwd())
    if os.path.isfile(path): #if it's pointing to a Vagrantfile - we want the directory name
        path = os.path.dirname(path)
    if not VAGRANT_FILE in os.listdir(path):
        print >>sys.stderr, 'Error: %s is not a valid path to a Vagrantfile or to a valid box directory' % path
        sys.exit(1)
    os.chdir(path)
    return os.path.join(path, BOX_FILE_NAME)


def package_box(path):
    validate_path(path)

    print 'Starting Box Packaing Process'
    print '\n====================================\n'
    #This should be replaced with a vagrant python wrapper rather than a shell command in the future
    output = run_cmd('vagrant', 'package')
    print output


def check_response(res):
    if not res.ok:
        print >>sys.stderr, 'Something went wrong. Received a %i return code' % res.status_code
        print >>sys.stderr, res.content
        sys.exit(1)


def create_version(version):
    print 'Attempting to create version %s' % version
    create_url = '%s/versions' % BASE_URL
    headers = {
               'X-Atlas-Token': ACCESS_TOKEN
    }
    data = {
      'version[version]': version
    }
    res = requests.post(create_url, headers=headers, data=data)
    check_response(res)
    return res


def create_provider(version):
    print 'Creating Provider...'
    create_url = '%s/version/%s/providers' % (BASE_URL, version)
    headers = {
               'X-Atlas-Token': ACCESS_TOKEN
    }
    data = {
        'provider[name]': PROVIDER
    }
    res = requests.post(create_url, headers=headers, data=data)
    check_response(res)
    return res


def get_upload_status(version):
    print 'Getting Upload Status...'
    status_url = '%s/version/%s/provider/virtualbox/upload?access_token=%s'\
                    % (BASE_URL, version, ACCESS_TOKEN)
    res = requests.get(status_url)
    check_response(res)
    return res


def submit_upload(path, upload_url):
    print 'Uploading box file %s' % path
    #The requests mulitpart file upload is being rejected by the Vagrant API - Just using a curl shell command for now
    # upload_file = {'file': open(path)}
    # res = requests.put(upload_url, files=upload_file)
    # return res

    upload_response = run_cmd(CURL, '-X', 'PUT', '--upload-file', path, upload_url)


def release_version(version):
    print 'Releasing Version: %s' % version
    release_url = '%s/version/%s/release' % (BASE_URL, version)
    headers = {
               'X-Atlas-Token': ACCESS_TOKEN
    }
    res = requests.put(release_url, headers=headers)
    check_response(res)
    return res


def get_version_status(version):
    status_url = '%s/version/%s/provider/%s?access_token=%s' % (BASE_URL, version, PROVIDER, ACCESS_TOKEN)
    res = requests.get(status_url)
    check_response(res)
    return res


def upload_box(version, path):
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

    create_version_response = create_version(version)
    create_provider_response = create_provider(version)
    status_response = get_upload_status(version)
    status_data = status_response.json()

    if success_key in status_data:
        if not status_data[success_key]:
            print >>sys.stderr,'Errors: %s' % status_data[errors_key]
            sys.exit(1)
    upload_url   = status_data['upload_path']
    upload_token = status_data['token']

    submit_upload(path, upload_url)
    release_response = release_version(version)
    verification_response = get_version_status(version)
    hosted_token = verification_response.json()['hosted_token']

    if upload_token == hosted_token:
        print 'Successfully uploaded and released box %s/%s version %s' % (USER_NAME, BOX_NAME, version)
    else:
        print >>sys.stderr, 'The upload and hosted tokens do not match - Something went wrong with the upload and release process'
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Package and upload the kubos-sdk vagrant box and upload it to the Vagrant Cloud')

    parser.add_argument('version',
                        nargs=1,
                        help='Specify the version of the upload')

    parser.add_argument('--all',
                        action='store_true',
                        default=False,
                        help='Build and Upload the box to Atlas')

    parser.add_argument('--package',
                        action='store_true',
                        help='Only package the package.box image but do no upload it to the Vagrant Cloud')

    parser.add_argument('--upload',
                        action='store_true',
                        help='Skip the building and upload the box')

    parser.add_argument('--box',
                        metavar='PKG_PATH',
                        default=None,
                        help='Specify a non-default Vagrant box directory (points to a Vagrantfile or the directory containing the Vagrant file)')

    args, following_args = parser.parse_known_args()
    args = vars(args)

    all     = args['all']
    box     = args['box']
    build   = args['package']
    upload  = args['upload']
    version = args['version'][0]

    if build or all:
        package_box(box)
    if upload or all:
        upload_box(version, box)


if __name__ == '__main__':
    main()

