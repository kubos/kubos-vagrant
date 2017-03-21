#These start an interactive prompt - I can't figure out how to fix it yet...
sudo apt-mark hold grub-common grub-pc grub-pc-bin grub2-common

apt-get update
apt-get install -y software-properties-common

add-apt-repository -y ppa:team-gcc-arm-embedded/ppa
add-apt-repository -y ppa:george-edison55/cmake-3.x
add-apt-repository -y ppa:git-core/ppa
add-apt-repository -y ppa:fkrull/deadsnakes-python2.7
apt-get update

apt-get upgrade -y python2.7
apt-get install -y build-essential libssl-dev libffi-dev libhidapi-hidraw0
apt-get install -y python-setuptools build-essential ninja-build python-dev libffi-dev libssl-dev
apt-get install -y gcc-arm-embedded
apt-get install -y git
apt-get install -y cmake
apt-get install -y gcc-msp430 gdb-msp430 msp430-libc

# flash tools
apt-get install -y mspdebug
apt-get install -y dfu-util
apt-get install -y openocd

#Install kernel additions for better USB device recognition
apt-get install -y linux-image-extra-virtual

#libmsp430.so is mounted from the bin/ directory
apt-get install unzip
unzip libmsp430.so.zip
mv libmsp430.so /usr/lib
rm -rf libmsp430.so.zip libmsp430.so

#do the pip setup and installation things
easy_install pip
pip install --upgrade pip

#KubOS Linux setup
echo "Installing KubOS Linux Toolchain"

apt-get install -y minicom
apt-get install -y libc6-i386 lib32stdc++6 lib32z1

wget http://portal.kubos.co/bin/iobc_toolchain.tar.gz
tar -xf /home/vagrant/iobc_toolchain.tar.gz -C /usr/bin
rm /home/vagrant/iobc_toolchain.tar.gz
mv /home/vagrant/minirc.kubos /etc/minicom/minirc.kubos
mv /home/vagrant/ftdi-usb.rules /etc/udev/rules.d/ftdi-usb.rules
echo "export PATH=/usr/bin/iobc_toolchain/usr/bin:$PATH" >> /etc/profile
adduser vagrant dialout

#Vagrant commands may act funny without password-less sudo
echo "vagrant ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

echo "Finished root provisioning"
