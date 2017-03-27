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
import os
import sys
import shutil
import subprocess


class BoxAutomator(object):
    ACCESS_TOKEN = None
    BOX_NAME = 'kubos'
    BOX_FILE_NAME = 'package.box' # This is the default name given from `vagrant package`
    KUBOS_BUILD_DIR = 'KUBOS_BUILD_DIR'
    PROVIDER = 'virtualbox'
    USER_NAME = 'kubostech'
    VAGRANT_FILE  = 'Vagrantfile'
    VAGRANT_REPO_URL = 'https://github.com/kubostech/kubos-vagrant'
    BASE_URL = 'https://atlas.hashicorp.com/api/v1/box/%s/%s' % (USER_NAME, BOX_NAME)

    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.BASE_DIR = os.environ[self.KUBOS_BUILD_DIR] if self.KUBOS_BUILD_DIR in os.environ else os.path.dirname(__file__)
        self.BUILD_DIR = os.path.join(self.BASE_DIR, 'builds')
        self.VERSION_DIR = os.path.join(self.BUILD_DIR, self.version)
        self.LOG_DIR = os.path.join(self.VERSION_DIR, 'logs')
        self.setup_dirs()


    def setup_dirs(self):
        self.mkdir(self.BASE_DIR)
        self.mkdir(self.BUILD_DIR)
        self.mkdir(self.VERSION_DIR)
        self.VERSION_GIT_DIR = os.path.join(self.VERSION_DIR, '.git')
        os.chdir(self.VERSION_DIR)


    def check_log_dir(self):
        #Because cloning requires an empty directory we have to make the log directory at a later time.
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


    def mkdir(self, path):
        print 'maiking directory: %s' % path
        if not os.path.isdir(path):
            os.makedirs(path)


    def validate_path(self, path):
        if not path:
            print 'Path was not provided. Using the default path...'
            self.path = os.path.join(os.getcwd(), self.name)
        if os.path.isfile(self.path): #if it's pointing to a Vagrantfile - we want the directory name
            self.path = os.path.dirname(self.path)
        if not self.VAGRANT_FILE in os.listdir(self.path):
            print >>sys.stderr, 'Error: %s is not a valid path to a Vagrantfile or to a valid box directory' % path
            sys.exit(1)
        os.chdir(self.path)


    def validate_box_path(self, args):
        #validate_box_path is only called from the upload file - which requires a valid package.box file
        #to be functional
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


def clean_build(args):
    automator = BoxAutomator(args.version)
    automator.clean()

