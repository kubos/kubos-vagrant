#These start an interactive prompt - I can't figure out how to fix it yet...
sudo apt-mark hold grub-common grub-pc grub-pc-bin grub2-common

apt-get update
apt-get install -y software-properties-common

add-apt-repository -y ppa:team-gcc-arm-embedded/ppa
add-apt-repository -y ppa:george-edison55/cmake-3.x
apt-get update

apt-get upgrade -y python2.7 ncurses-dev bc
apt-get install -y build-essential libssl-dev libffi-dev libhidapi-hidraw0 gdb
apt-get install -y python-setuptools build-essential ninja-build python-dev libffi-dev libssl-dev
apt-get install -y gcc-arm-embedded
apt-get install -y git
apt-get install -y cmake
apt-get install -y gcc-msp430 gdb-msp430 msp430-libc
apt-get install -y libdbus-1-dev dbus

# flash tools
apt-get install -y mspdebug
apt-get install -y dfu-util
apt-get install -y openocd

#Install kernel additions for better USB device recognition
apt-get install -y linux-image-extra-virtual

#libmsp430.so is mounted from the bin/ directory
mv /home/vagrant/libmsp430.so /usr/lib

#do the pip setup and installation things
easy_install pip
# Need to install pip<v10 due to this issue: https://github.com/ARMmbed/yotta/issues/835
# Forcibly controlling version until this is resolved
pip install pip==9.0.3

#sqlite
apt-get install -y sqlite3 libsqlite3-dev

#documentation tools
apt-get install -y doxygen graphviz plantuml
pip install Sphinx==1.5.6
pip install breathe
pip install sphinx-rtd-theme==0.2.4
pip install sphinxcontrib-plantuml
pip install sphinx-jsondomain

#KubOS Linux setup
echo "Installing KubOS Linux Toolchains"

apt-get install -y minicom
apt-get install -y libc6-i386 lib32stdc++6 lib32z1

#Utilities for building KubOS Linux
apt-get install -y unzip mtools

#iOBC Toolchain
wget https://s3.amazonaws.com/provisioning-kubos/iobc_toolchain.tar.gz
tar -xf /home/vagrant/iobc_toolchain.tar.gz -C /usr/bin
rm /home/vagrant/iobc_toolchain.tar.gz
echo "export PATH=$PATH:/usr/bin/iobc_toolchain/usr/bin" >> /etc/profile

#Beaglebone Black/Pumpkin MBM2 toolchain
wget https://s3.amazonaws.com/provisioning-kubos/bbb_toolchain.tar.gz
tar -xf /home/vagrant/bbb_toolchain.tar.gz -C /usr/bin
rm /home/vagrant/bbb_toolchain.tar.gz

#Legacy Beaglebone Black toolchain
apt-get install -y crossbuild-essential-armhf gcc-arm-linux-gnueabihf g++-arm-linux-gnueabihf

mv /home/vagrant/minirc.kubos /etc/minicom/minirc.kubos
mv /home/vagrant/minirc.msp430 /etc/minicom/minirc.msp430
mv /home/vagrant/kubos-usb.rules /etc/udev/rules.d/kubos-usb.rules
mv /home/vagrant/kubos-dbus.conf /etc/dbus-1/kubos-dbus.conf
mv /home/vagrant/dbus_setup.sh /etc/dbus-1/dbus_setup.sh

adduser vagrant dialout

#Lua setup
cd /usr/local/bin && curl -L https://github.com/luvit/lit/raw/master/get-lit.sh | sh
rm /usr/local/bin/luvi
cd /usr/local/bin && wget https://github.com/luvit/luvi-binaries/raw/master/Linux-x86_64/luvi-regular
chmod a+x /usr/local/bin/luvi-regular

#Vagrant commands may act funny without password-less sudo
echo "vagrant ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

echo "Finished root provisioning"
