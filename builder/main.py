import argparse

from provision import BoxProvisioner
from package import package_box

def provision(args):
    provisioner = BoxProvisioner(args.version)
    #initial provisioning
    provisioner.run_provision_step('initial', provision_with=['privileged', 'non-privileged'])
    #test
    provisioner.run_provision_step('test', provision_with=['test'])
    # #pre-package
    provisioner.run_provision_step('pre-package', provision_with=['pre-package'])


def package(args):
    package_box(args)


def upload(args):
    run_upload(args)


def main():
    #TODO: All the argparse things
    parser = argparse.ArgumentParser(
        description='Package and upload the kubos-sdk vagrant box and upload it to the Vagrant Cloud')

    parser.add_argument('version',
                        nargs=1,
                        help='Specify the version of the upload')

    parser.add_argument('--all',
                        action='store_true',
                        default=False,
                        help='Provision, Package and Upload the box to Atlas')

    parser.add_argument('--provision-only',
                        action='store_true',
                        default=False,
                        help='Only provision the box but do not package or upload it')

    parser.add_argument('--package-only',
                        action='store_true',
                        default=False,
                        help='Only package the package.box image but do no upload it to the Vagrant Cloud')

    parser.add_argument('--upload-only',
                        action='store_true',
                        default=False,
                        help='Skip the building and upload the box')

    #The following 2 options are useful when an upload fails and needs to be re-run
    #Creating either the version or provider twice will cause a failure
    parser.add_argument('--upload-no-create-version',
                        action='store_true',
                        default=False,
                        help='Skip creating the version when uploading the box')

    parser.add_argument('--upload-no-create-provider',
                        action='store_true',
                        default=False,
                        help='Skip creating the provider when uploading the box')

    parser.add_argument('--upload-no-box-upload',
                        action='store_true',
                        default=False,
                        help='Skip the box upload step of the upload process')

    parser.add_argument('--upload-no-release',
                        action='store_true',
                        default=False,
                        help='Skip the release step after uploading the box')

    parser.add_argument('--box',
                        default=None,
                        help='Specify a non-default Vagrant box directory (points to a Vagrantfile or the directory containing the Vagrant file)')

    args, following_args = parser.parse_known_args()
    args.version = args.version[0] #version is initally a list of 1 element
    if args.all or args.provision_only:
        provision(args)
    if args.all or args.package_only:
        package(args)
    if args.all or args.upload_only:
        upload(args)

if __name__ == '__main__':
    main()
