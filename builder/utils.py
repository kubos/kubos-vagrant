import git
import os
import sys
import subprocess

VAGRANT_FILE  = 'Vagrantfile'

class BoxAutomator(object):
    ACCESS_TOKEN = None
    BOX_NAME = 'kubos'
    BOX_FILE_NAME = 'package.box' # This is the default name given from `vagrant package`
    CURL = 'curl'
    PROVIDER = 'virtualbox'
    USER_NAME = 'kubostech'

    BASE_URL = 'https://atlas.hashicorp.com/api/v1/box/%s/%s' % (USER_NAME, BOX_NAME)

    def __init__(self, version):
        self.BASE_DIR = os.environ[self.KUBOS_BUILD_DIR] if self.KUBOS_BUILD_DIR in os.environ else os.getcwd()
        self.BUILD_DIR = os.path.join(self.BASE_DIR, 'builds')
        self.VERSION_DIR = os.path.join(self.BUILD_DIR, self.version)
        self.LOG_DIR = os.path.join(self.VERSION_DIR, 'logs')
        self.version = version
        self.setup_dirs()


    def setup_dirs(self):
        mkdir(self.BASE_DIR)
        mkdir(self.BUILD_DIR)
        mkdir(self.VERSION_DIR)
        self.VERSION_GIT_DIR = os.path.join(self.VERSION_DIR, '.git')

        # repo = clone_repo(VERSION_DIR, VAGRANT_REPO_URL)
        mkdir(self.LOG_DIR)
        # checkout_tag(temp_version)
        os.chdir(self.VERSION_DIR)


    def clone_repo(self, repo_dir, repo_url):
        try:
            repo_git_dir = os.path.join(repo_dir, '.git')
            if not os.path.isdir(repo_git_dir):
                repo = git.Repo.clone_from(repo_url, repo_dir)
                print 'Successfully cloned repo: %s' % repo_url
            else:
                repo = git.Repo(repo_dir)
            fetch_tags(repo)
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
        if not os.path.isdir(path):
            os.makedirs(path)


    def validate_path(self, path):
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


    def run_cmd(self, *args, **kwargs):
        cwd = kwargs.get('cwd', os.getcwd())

        print ' '.join(args)

        try:
            return subprocess.check_output(args, **kwargs)
        except subprocess.CalledProcessError, e:
            print >>sys.stderr, 'Error executing command %s' % (args)
            sys.exit(1)

