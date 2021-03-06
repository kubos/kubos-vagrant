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

import json
import os
import subprocess
import sys
import vagrant

from utils import BoxAutomator

class BoxProvisioner(BoxAutomator):
    STATUS_KEY = 'provision'
    VAGRANT_REPO_URL = 'https://github.com/kubos/kubos-vagrant'
    DUMP_LOG_LINES = 50 # Number of lines to dump from end of logs on an error
    status_steps = {
                        'base' :      ['file',
                                       'privileged',
                                       'test',
                                       'pre-package'],
                        'kubos-dev' : ['file',
                                       'privileged',
                                       'non-privileged',
                                       'test',
                                       'pre-package']
                      }

    def __init__(self, args):
        super(BoxProvisioner, self).__init__(args)


    def clone_vagrant_repo(self):
        if not os.path.isfile(self.VERSION_GIT_DIR):
            self.clone_repo(self.VERSION_DIR, self.VAGRANT_REPO_URL)
        self.post_clone_setup()
        self.setup_status()


    def run_provision_step(self, step, **kwargs):
        if self.resume:
            res = self.check_status(step)
            if res == True:
                print("Step {} already performed.. Skipping..".format(step))
                return
            if res == None:
                self.setup_status_file()
                self.run_provision_step(step)
        self.check_log_dir()
        self.step_log = os.path.join(self.LOG_DIR, step + '-' + 'output.log')
        log_cm = vagrant.make_file_cm(self.step_log)
        print('Logging to file: {}'.format(self.step_log))
        v = vagrant.Vagrant(out_cm=log_cm, err_cm=log_cm)
        try:
            v.up(provision_with=[step], **kwargs)
            self.update_status(step)
        except subprocess.CalledProcessError as e:
            print('Error: The provision step {} failed with error code {}.'.format(step, e.returncode), file=sys.stderr)
            self.dump_log()
            sys.exit(1)


    def dump_log(self):
        print('Dumping last {} lines of log: {}\n\n'.format(self.DUMP_LOG_LINES, self.step_log))
        print(self.run_cmd('tail', '-n', '{}'.format(self.DUMP_LOG_LINES), self.step_log))


    def provision(self):
        self.box_dir = os.path.join(os.getcwd(), self.name)
        if not os.path.isdir(self.box_dir):
            print("The requested box directory: {} does not exist".format(self.box_dir), file=sys.stderr)
            sys.exit(1)
        os.chdir(self.box_dir)
        self.post_clone_setup()
        steps = self.status_steps[self.name]
        for step in steps:
            self.run_provision_step(step)


    def run_initial_provision(self):
        self.run_provision_step('initial', provision_with=['privileged', 'non-privileged'])


    def run_test_provision(self):
        self.run_provision_step('test', provision_with=['test'])


    def run_pre_package_provision(self):
        self.run_provision_step('pre-package', provision_with=['pre-package'])


def provision_box(args):
    provisioner = BoxProvisioner(args)
    if args.local:
        provisioner.copy_box_directory(args.box_name)
        provisioner.setup_status()
    else:
        provisioner.clone_vagrant_repo()
    provisioner.provision()
    print('Provisioning successfully completed...')

