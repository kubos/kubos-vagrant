import argparse
import git
import os
import vagrant
import subprocess
import sys
from utils import BoxAutomator


class BoxProvisioner(BoxAutomator):
    version = '0.0.0' #TODO get this from a cmd line arg
    KUBOS_BUILD_DIR = 'KUBOS_BUILD_DIR'
    VAGRANT_REPO_URL = 'https://github.com/kubostech/kubos-vagrant'


    def run_provision_step(self, step, **kwargs):
        self.step_log = os.path.join(self.LOG_DIR, step)
        log_cm = vagrant.make_file_cm(self.step_log + '-' + 'output.log')
        print ' logging to file: %s' % self.step_log + '-' + 'output.log'
        v = vagrant.Vagrant(out_cm=log_cm, err_cm=log_cm)
        try:
            v.up(**kwargs)
        except subprocess.CalledProcessError as e:
            print>>sys.stderr, 'Error: The provision step %s failed with error code %i. See the provision log for details: %s' % (step, e.returncode, self.step_log)


