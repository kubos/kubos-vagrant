import argparse
from utils import clean_build
from provision import provision_box
from package   import package_box
from uploader  import upload_box


def main():
    parser = argparse.ArgumentParser(
        description='Package and upload the kubos-sdk vagrant box and upload it to the Vagrant Cloud')

    parser.add_argument('version',
                        nargs=1,
                        help='Specify the version of the upload')

    parser.add_argument('--all',
                        action='store_true',
                        default=False,
                        help='Provision, Package and Upload the box to Atlas')

    parser.add_argument('--clean',
                        action='store_true',
                        default=False,
                        help='Delete any pre-existing build files for this version and rebuild from scratch')

    parser.add_argument('--provision',
                        action='store_true',
                        default=False,
                        help='Only provision the box but do not package or upload it')

    parser.add_argument('--provision-no-clone',
                        action='store_true',
                        default=False,
                        help='Provision the box without trying to reclone the repo')

    parser.add_argument('--package',
                        action='store_true',
                        default=False,
                        help='Only package the package.box image but do no upload it to the Vagrant Cloud')

    parser.add_argument('--upload',
                        action='store_true',
                        default=False,
                        help='Skip the provisioning and building steps. Only upload the box')

    #The following 2 options are useful when an upload fails and needs to be re-run
    #Creating either the version or provider twice will cause a failure
    parser.add_argument('--upload-no-create-version',
                        action='store_false',
                        default=True,
                        help='Skip creating the version when uploading the box')

    parser.add_argument('--upload-no-create-provider',
                        action='store_false',
                        default=True,
                        help='Skip creating the provider when uploading the box')

    parser.add_argument('--upload-no-box-upload',
                        action='store_false',
                        default=True,
                        help='Skip the box upload step of the upload process')

    parser.add_argument('--upload-no-release',
                        action='store_false',
                        default=True,
                        help='Skip the release step after uploading the box')

    parser.add_argument('--box',
                        default=None,
                        help='Specify a non-default Vagrant box directory (points to a Vagrantfile or the directory containing the Vagrant file)')

    args, following_args = parser.parse_known_args()
    args.version = args.version[0] #version is initally a list of 1 element
    if args.clean_build:
        clean_build(args)

    if args.all or args.provision_only:
        provision_box(args)
    if args.all or args.package_only:
        package_box(args)
    if args.all or args.upload_only:
            upload_box(args)

if __name__ == '__main__':
    main()
