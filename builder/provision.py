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
        if self.name == 'kubos-dev':
            # Pull the latest base box if there's a new one available
            # Vagrant doesn't allow tagging local boxes with version #'s
            self.update_base_box()


    def update_base_box(self):
        print 'Updating the base box'
        self.run_cmd('vagrant', 'box', 'update', '--box', 'kubos/base', '--provider', 'virtualbox')


    def clone_vagrant_repo(self):
        if not os.path.isfile(self.VERSION_GIT_DIR):
            self.clone_repo(self.VERSION_DIR, self.VAGRANT_REPO_URL)
        self.post_clone_setup()
        self.setup_status()


    def run_provision_step(self, step, **kwargs):
        if self.resume:
            res = self.check_status(step)
            if res == True:
                print "Step %s already performed.. Skipping.." % step
                return
            if res == None:
                self.setup_status_file()
                self.run_provision_step(step)
        self.check_log_dir()
        self.step_log = os.path.join(self.LOG_DIR, step + '-' + 'output.log')
        log_cm = vagrant.make_file_cm(self.step_log)
        print 'Logging to file: %s' % self.step_log
        v = vagrant.Vagrant(out_cm=log_cm, err_cm=log_cm)
        try:
            v.up(provision_with=[step], **kwargs)
            self.update_status(step)
        except subprocess.CalledProcessError as e:
            print>>sys.stderr, 'Error: The provision step %s failed with error code %i.' % (step, e.returncode)
            self.dump_log()
            sys.exit(1)


    def dump_log(self):
        print 'Dumping last %i lines of log: %s\n\n' %  (self.DUMP_LOG_LINES, self.step_log)
        print self.run_cmd('tail', '-n', '%i' % self.DUMP_LOG_LINES, self.step_log)


    def provision(self):
        self.box_dir = os.path.join(os.getcwd(), self.name)
        if not os.path.isdir(self.box_dir):
            print >>sys.stderr, "The requested box directory: %s does not exist" % self.box_dir
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
    print 'Provisioning successfully completed...'

