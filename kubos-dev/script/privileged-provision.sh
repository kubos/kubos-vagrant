#!/bin/bash
set -ex

# These start an interactive prompt - I can't figure out how to fix it yet...
sudo apt-mark hold grub-common grub-pc grub-pc-bin grub2-common

apt-get update -y
apt-get install -y software-properties-common

apt-get upgrade -y python3.5 ncurses-dev bc
apt-get install -y build-essential libssl-dev libffi-dev libhidapi-hidraw0 gdb
apt-get install -y build-essential ninja-build python-dev libffi-dev libssl-dev pkg-config
apt-get install -y git
apt-get install -y cmake
apt-get install -y sshpass
# resolvconf is no longer included by default as of Ubuntu 18.04
apt-get install -y resolvconf
rm -f /etc/resolv.conf
# There's something wrong with the default resolv.conf symlink. This fixes it
ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf

# Install kernel additions for better USB device recognition
apt-get install -y linux-image-extra-virtual

# Do the pip setup and installation things
apt-get install -y python3-pip python3-setuptools

pip3 install wheel

# Install all Kubos python dependencies
git clone https://github.com/kubos/kubos --depth 1
pip3 install -r kubos/requirements.txt
rm -r kubos

# sqlite
apt-get install -y sqlite3 libsqlite3-dev

# Documentation tools
apt-get install -y doxygen graphviz plantuml

# KubOS Linux setup
echo "Installing KubOS Linux Toolchains"

apt-get install -y minicom
apt-get install -y libc6-i386 lib32stdc++6 lib32z1

# Utilities for building KubOS Linux
apt-get install -y unzip mtools

# iOBC Toolchain
wget https://s3.amazonaws.com/kubos-world-readable-assets/iobc_toolchain.tar.gz
tar -xf /home/vagrant/iobc_toolchain.tar.gz -C /usr/bin
rm /home/vagrant/iobc_toolchain.tar.gz
echo "export PATH=$PATH:/usr/bin/iobc_toolchain/usr/bin" >> /etc/profile

# Beaglebone Black/Pumpkin MBM2 toolchain
wget https://s3.amazonaws.com/kubos-world-readable-assets/bbb_toolchain.tar.gz
tar -xf /home/vagrant/bbb_toolchain.tar.gz -C /usr/bin
rm /home/vagrant/bbb_toolchain.tar.gz

mv /home/vagrant/minirc.kubos /etc/minicom/minirc.kubos
mv /home/vagrant/kubos-usb.rules /etc/udev/rules.d/kubos-usb.rules

adduser vagrant dialout

#Vagrant commands may act funny without password-less sudo
echo "vagrant ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

mkdir -p /home/vagrant/.kubos
git clone https://github.com/kubos/kubos /home/vagrant/.kubos/kubos --depth 1
chown -R vagrant /home/vagrant/.kubos

echo "Finished root provisioning"
