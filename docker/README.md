This folder contains a docker environment for developing KubOS. 

It consists of a couple docker containers and a script of some kind (currently docker compose) to make the experience as similar as possible to "vagrant up".

## Containers
The top level dockerfile is for the `kubos-dev` image and is meant to be a base image suitable for expanding on or using for things like CI builds.

inside the `sdk` dir you will find a dockerfile for a `kubos-sdk` image that builds off of this base to  hopefully attempt to do a better job at emulating the Kubos SDK (and the KubOS environment) by doing things like setting up users and home directories.

## Setup
### Building the images
to build the container run `docker build -t <name> .` while inside the folder for the container you want to build. You need to build kubos-dev first before any containers that rely on it.

Alternatively, just use the `build.sh` script to build all the containers

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

