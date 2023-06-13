This folder contains a docker environment for developing KubOS. 

It consists of a couple docker containers and a script of some kind (currently docker compose) to make the experience as similar as possible to "vagrant up".

## Containers
There are three containers at play here to keep things organized:

**kubos-base** - a base image containing dependencies that must be installed from a priviliged account (root)

**kubos-build** - this image is intended to be a replica of what is currently being used for CI builds

**kubos-sdk** - this image is intended to emulate the KubOS SDK vagrant envrionment as closely as possible and installs many dependencies under a regular user account

## Setup
### Building the images

**TL;DR** to build any of the docker containers, use the command `docker build -t <image_name> -f <image_folder>/Dockerfile . ` while inside this `docker` folder. if you are just looking to build the docker container for the SDK, theres also a `build-sdk.sh` script.

This slightly different command from the usual `docker build -t <name> .` is needed because the various containers need to copy some fonfiguration files from the `bin` folder throughout the process, so this folder also needs to be part of dockers build context.

The build context is the directory passed to `docker build`, which is where it looks for the `Dockerfile` by default. Because this `bin` folder and the `Dockerfile` are in separate directories, the build context should be set to the `docker` folder and the Dockerfile needs to be manually specified because it differs from the default.

#### Image names
Most of the images rely on the `kubos-base` image, so it is recommended to keep the image names the same as the directory of their `Dockerfile` so images like `kubos-sdk` that depend on this base image are still able to build correctly.
### Configuring the container

Because the docker compose file is designed to be run from the directory you want to mount (similar to the Vagrantfile), it should be relocated there.

If you want a one-time setup, use this copy command from this directory to create or replace your docker compose in your desired location: `cp ./docker-compose.yml /path/to/your/Vagrantfile`

If you want to automatically keep things in sync, use a symlink: `ln -s /full/path/to/docker/docker-compose.yml ./path/to/your/Vagrantfile`

### Running the container
To get a shell into the container similar to vagrant ssh, use `docker-compose run --rm kubos-sdk` from the directory where you copoed the compose file to.

The docker container will auto-mount this directory into the container at the mount point /vagrant just like the KubOS Vagrant SDK.

To add additional directory mounts, such as for mounting something to `/home/kubos`, feel free to edit the `docker-compose.yml`

## Transferring data from the VM
Vagrant offers a plugin that can be used to exfiltrate the data you want to transfer to the docker environment. This can be set up using `vagrant plugin install vagrant-scp` ([source](https://stackoverflow.com/questions/16704059/easiest-way-to-copy-a-single-file-from-host-to-vagrant-guest#28359455))


## Moving the generated image to an external drive
For space-constrained host PC's, its possible to move the docker images to an external drive:
- Macos: https://stackoverflow.com/questions/38205735/store-docker-image-files-on-external-drive-in-macos#40114330
- linux:

