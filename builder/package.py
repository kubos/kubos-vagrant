import vagrant
import utils

def package_box(args):
    utils.validate_path(args.box)

    print 'Starting Box Packaging Process'
    print '\n====================================\n'
    v = Vagrant()
    try:
        v.package()
    except subprocess.CalledProcessError as e:
        print>>sys.stderr, 'Error: The package step failed'



