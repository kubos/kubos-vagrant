For use instructions checkout the official [Kubos docs](http://docs.kubos.co/1.1.0/sdk-docs/index.html)

## Testing Vagrant Changes:

For testing changes in the `kubos-dev` box only skip ahead to the "Testing kubos-dev changes" section. The `kubos-dev` box is built on top of the `base` box. When the `kubos-dev` box is build, the `base` box image is booted and then modified to produce the new `kudos-dev` image. Therefore, changes to the `base` box require a rebuild of the `kubos-dev` box.

## Testing Base Box Changes

For testing the changes in the `base` box modify the Vagrantfile and provisioning scripts in the `base/` directory as needed. To test these changes in isolation from the `kubos-dev` box run:

    $ vagrant build

NOTE: To rebuild the image run `vagrant destroy` followed by `vagrant build`.

To apply these base changes to a `kudos-dev` build you must create a .box image. In the `kubos-vagrant/base/` directory run:

    $ vagrant package

This will take a while. It will produce a package.box artifact in the same directory the command is run from.

Once it completes we have to add the base image to vagrant. If you have existing base box images (`vagrant box list` will show you if you do) you must remove them as vagrant will default to the latest base box version of a box. Adding a box locally (like we are about to) doesn’t support manually specifying the box version.

To remove the existing `base` images, if you have them, run:

    $ vagrant box remove kubos/base [--all]

NOTE: `--all` will remove all versions of that box if you have multiple versions and want to remove them with one command

Add the new base box image:

    $ vagrant box add kubos/base <Path to package.box from previous `vagrant package` command>

Continue on to the next section.

## Testing kudos-dev changes

Modify the Vagrantfile and provisioning scripts in `kubos-vagrant/kubos-dev/` as needed.

You can rebuild the image to test locally using:

    $ vagrant build

To rebuild the image run `vagrant destroy` followed by `vagrant build`.

:shipit:

TODO: Fix the build script and add release instructions here