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

import os
import subprocess
import sys
import vagrant

from utils import BoxAutomator

class BoxProvisioner(BoxAutomator):

    def __init__(self, version):
        super(BoxProvisioner, self).__init__(version)


    def clone_vagrant_repo(self):
        if not os.path.isfile(self.VERSION_GIT_DIR):
            self.clone_repo(self.VERSION_DIR, self.VAGRANT_REPO_URL)
        # checkout_tag(self.version)

    def run_provision_step(self, step, **kwargs):
        self.check_log_dir()
        self.step_log = os.path.join(self.LOG_DIR, step)
        log_cm = vagrant.make_file_cm(self.step_log + '-' + 'output.log')
        print 'logging to file: %s' % self.step_log + '-' + 'output.log'
        v = vagrant.Vagrant(out_cm=log_cm, err_cm=log_cm)
        try:
            v.up(**kwargs)
        except subprocess.CalledProcessError as e:
            print>>sys.stderr, 'Error: The provision step %s failed with error code %i.\nSee the provision log for details: %s' % (step, e.returncode, self.step_log)
            sys.exit(1)


    def run_initial_provision(self):
        self.run_provision_step('initial', provision_with=['privileged', 'non-privilegjd'])


    def run_test_provision(self):
        self.run_provision_step('test', provision_with=['test'])


    def run_pre_package_provision(self):
        self.run_provision_step('pre-package', provision_with=['pre-package'])


def provision_box(args):
    provisioner = BoxProvisioner(args.version)
    if not args.provision_no_clone:
        provisioner.clone_vagrant_repo()
    provisioner.run_initial_provision()
    provisioner.run_test_provision()
    provisioner.run_pre_package_provision()
    print 'Provisioning successfully completed...'

