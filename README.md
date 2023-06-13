##  Kubos-Dev

This repo aims to contain various dev and build environment setup instructions.

It includes:
- the kubos vagrant environment mentioned in the kubos docs (`kubos-dev`)
- docker images for CI builds (`docker/kubos-build`) that have been relocated from the main repo
- a docker image that aims to be an equivalent to the vagrant image to promote reuse and space savings by deduplicating many things with the CI build image (`docker/kobos-sdk`) 


------


For usage instructions checkout the official [Kubos docs](https://docs.kubos.com/latest/sdk-docs/index.html)

## Testing Vagrant Changes:

For testing the changes in the `kubos-dev` box, modify the Vagrantfile and provisioning scripts in the `kubos-dev/` directory as needed.

You can rebuild the image to test locally by running the follow commands in the `kubos-dev/` folder:

    $ vagrant destroy

Followed by:

    $ vagrant up

After building a new vagrant, run the following command to get inside of the newly created box:

    $ vagrant ssh

You should now have an ssh session in the vagrant box. It is recommended to run through the CI tests, documentation generation,
and basic hardware interaction to verify that the box is working correctly.

## Building Vagrant Releases

The scripts for building and packaging a Vagrant box for release are found in the `builder/` directory.

The `main.py` script will be used when creating a Vagrant release.
It requires a version and an action.

Building a release based off local changes:

    $ ./main.py -al [version]

Building a release off of master:

    $ ./main.py -a [version]

Newly created releases will be found in the following location:

    builder/[version]/kubos-dev/package.box

## Uploading Vagrant Releases

The process for uploading a new Vagrant release is currently a manual one.

- Navigate to https://app.vagrantup.com/kubos/kubos-dev in your browser of choice.
- Click `New Version` at the top.
- Enter a version number and click `Create Version`.
- Click `Add a provider` on the newly created version's page.
- Type `virtualbox` into the `Provider` text field.
- Make sure `Upload to Vagrant Cloud` is selected next to `File Hosting` and click `Continue to Upload`.
- Under `Add Provider File`, click `Choose File` and select the `package.box` file found in the `builder` folder.
- Wait for the upload to complete. It will say `Upload Complete` next to `Status`.
- Click the `kubos-dev` link at the top of the page. You should see a list of available versions.
- The newly created version will be there with `unreleased` next to it. Click the `Release` button.
- This will take you to the `Release Box Version` page. Click `Release version` to make the release available.

## Updating Python requirements

Python requirements are maintained using the [pip-tools](https://github.com/jazzband/pip-tools) toolchain. See [pip-tools#installation](https://github.com/jazzband/pip-tools#installation). The `requirements.txt` file is generated using to `pip-compile` command from the list of dependencies specified in `requirements.in`. To update requirements, run:

```
pip-compile --output-file requirements.txt requirements.in
```
