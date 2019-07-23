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

import git
import json
import os
import sys
import shutil
import subprocess


class BoxAutomator(object):
    ACCESS_TOKEN = None
    STATUS_FILE_NAME = 'status.json'
    KUBOS_BUILD_DIR = 'KUBOS_BUILD_DIR'
    VAGRANT_FILE  = 'Vagrantfile'
    resume = True

    def __init__(self, args):
        self.name = args.box_name
        self.version = args.version
        self.resume = args.resume
        self.BASE_DIR = os.environ[self.KUBOS_BUILD_DIR] if self.KUBOS_BUILD_DIR in os.environ else os.path.dirname(__file__)
        self.BUILD_DIR = os.path.join(self.BASE_DIR, 'builds')
        self.VERSION_DIR = os.path.join(self.BUILD_DIR, self.version)
        self.STATUS_FILE = os.path.join(self.VERSION_DIR, self.STATUS_FILE_NAME)
        self.LOG_DIR = os.path.join(self.VERSION_DIR, 'logs')
        self.setup_dirs()


    def setup_dirs(self):
        self.mkdir(self.BASE_DIR)
        self.mkdir(self.BUILD_DIR)
        self.mkdir(self.VERSION_DIR)
        self.VERSION_GIT_DIR = os.path.join(self.VERSION_DIR, '.git')
        os.chdir(self.VERSION_DIR)

    '''
    Status Functions
    '''

    def load_status(self, path):
        if os.path.isfile(path):
            with open(path,'r') as data_file:
                try:
                    data = json.loads(data_file.read())
                    return data
                except:
                    return None
        return None


    def check_status(self, status_step):
        data = self.load_status(self.STATUS_FILE)
        if data == None:
            return None
        if status_step in data[self.name][self.STATUS_KEY]:
            return data[self.name][self.STATUS_KEY][status_step]
        else:
            return None


    def save_status(self, status, path):
        # Status is a json encoded dict
        with open(path, 'w') as status_file:
            status_file.write(json.dumps(status))


    def setup_status_file(self):
        if os.path.isfile(self.STATUS_FILE):
            data = self.load_status(self.STATUS_FILE)
            if data is not None and not self.name in data:
                data[self.name] = {}
                self.save_status(data, self.STATUS_FILE)
        else:
            # The status file doesn't exist. Create it and add the current box to it.
            js_data = json.loads('{ "%s" : {} }' % self.name)
            self.save_status(js_data, self.STATUS_FILE)


    def setup_status(self):
        if not os.path.isfile(self.STATUS_FILE):
            self.setup_status_file()

        data = self.load_status(self.STATUS_FILE)
        if self.STATUS_KEY not in data[self.name]:
            data[self.name][self.STATUS_KEY] = {}

        for step in self.status_steps[self.name]:
            if step in data[self.name][self.STATUS_KEY]:
                continue
            else:
                data[self.name][self.STATUS_KEY][step] = False
        self.save_status(data, self.STATUS_FILE)


    def update_status(self, step):
        # Updating the status upon completion of a step
        data = self.load_status(self.STATUS_FILE)
        data[self.name][self.STATUS_KEY][step] = True
        self.save_status(data, self.STATUS_FILE)

    '''
    Git utility functions
    '''

    def post_clone_setup(self):
        # Because cloning requires an empty directory we have to make the log directory at a later time.
        self.check_log_dir()
        self.setup_status_file()


    def check_log_dir(self):
        if not os.path.isdir(self.LOG_DIR):
            self.mkdir(self.LOG_DIR)


    def clone_repo(self, repo_dir, repo_url):
        try:
            repo_git_dir = os.path.join(repo_dir, '.git')
            if not os.path.isdir(repo_git_dir):
                repo = git.Repo.clone_from(repo_url, repo_dir)
                print 'Successfully cloned repo: %s' % repo_url
            else:
                repo = git.Repo(repo_dir)
            self.fetch_tags(repo)
            return repo
        except git.exc.GitCommandError as e:
            print 'Error: there was an error accessing the remote git repository...'
            print 'The specific error is: \n\n %s' % e


    def fetch_tags(self, repo):
        origin = repo.remotes.origin
        print 'Pulling latest tags..'
        origin.fetch()


    def checkout_tag(self, ref):
        try:
            repo.git.checkout(ref)
        except:
            print 'There was an error checking out branch "%s"' % ref
            print 'The error details are: %s' %  sys.exc_info()[0]


    '''
    Generic utility functions
    '''

    def mkdir(self, path):
        print 'making directory: %s' % path
        if not os.path.isdir(path):
            os.makedirs(path)


    def validate_path(self, path):
        if not path:
            print 'Path was not provided. Using the default path...'
            self.path = os.path.join(os.getcwd(), self.name)
        if os.path.isfile(self.path): # If it's pointing to a Vagrantfile - we want the directory name
            self.path = os.path.dirname(self.path)
        if not self.VAGRANT_FILE in os.listdir(self.path):
            print >>sys.stderr, 'Error: %s is not a valid path to a Vagrantfile or to a valid box directory' % path
            sys.exit(1)
        os.chdir(self.path)


    def validate_box_path(self, args):
        # Validate_box_path is only called from the upload file - which requires a valid package.box file
        # to be functional
        self.validate_path(args.box)
        self.box_path = os.path.join(self.path, self.BOX_FILE_NAME)
        if not os.path.isfile(self.box_path):
            print >> sys.stderr, 'Error: The requested upload path: %s is not a vaild package.box file' % self.box_path


    def run_cmd(self, *args, **kwargs):
        cwd = kwargs.get('cwd', os.getcwd())
        print ' '.join(args)

        try:
            return subprocess.check_output(args, **kwargs)
        except subprocess.CalledProcessError, e:
            print >>sys.stderr, 'Error executing command %s' % (args)
            sys.exit(1)


    def clean(self):
        if os.path.isdir(self.VERSION_DIR):
            print 'Cleaning existing build directory %s' % self.VERSION_DIR
            shutil.rmtree(self.VERSION_DIR)
            self.setup_dirs()


    def copy_box_directory(self, box_name):
        dest_dir = os.path.join(self.VERSION_DIR, box_name)
        source_dir = os.path.abspath(os.path.join(__file__, '..', '..', box_name))
        if os.path.isdir(dest_dir):
            print 'Destination directory %s already exists... Skipping copy' % dest_dir
        else:
            shutil.copytree(source_dir, dest_dir)


def clean_build(args):
    automator = BoxAutomator(args.version)
    automator.clean()

