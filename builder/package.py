import vagrant
from utils import BoxAutomator

class BoxPackager(BoxAutomator):

    def __init__(self, version):
        super(BoxPackager, self).__init__(version)


    def package(self, args):
        self.validate_path(args.box)

        print 'Starting Box Packaging Process'
        print '\n====================================\n'
        v = vagrant.Vagrant()
        try:
            v.package()
            print 'Packaging completed successfully...'
        except subprocess.CalledProcessError as e:
            print>>sys.stderr, 'Error: The package step failed'


def package_box(args):
    packager = BoxPackager(args.version)
    packager.package(args)

