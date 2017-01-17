apt-get update
apt-get -y dist-upgrade
apt-get update
add-apt-repository -y ppa:team-gcc-arm-embedded/ppa
add-apt-repository -y ppa:george-edison55/cmake-3.x
add-apt-repository -y ppa:git-core/ppa
add-apt-repository ppa:fkrull/deadsnakes-python2.7
apt-get update

apt-get upgrade -y python2.7
apt-get -y install build-essential libssl-dev libffi-dev libhidapi-hidraw0
apt-get install -y python-setuptools build-essential ninja-build python-dev libffi-dev libssl-dev
apt-get install -y gcc-arm-embedded
apt-get -y install python-pip
apt-get -y install git
apt-get install -y cmake
apt-get install -y gcc-msp430 gdb-msp430 msp430-libc

# flash tools
apt-get install -y mspdebug
apt-get install -y dfu-util
apt-get install -y openocd

#Install kernel additions for better USB device recognition
apt-get install -y linux-image-extra-virtual

#Since this is a private repo the url is unavailable without authentication. An alternate temporary solution is on lines #31-35
# download libmsp430.so
#wget -P /usr/lib https://github.com/kubostech/kubos/raw/vagrant-provision/vm/lib/libmsp430.so

#Temporary fix for private repo hosting the libmsp430.so binary
apt-get install unzip
wget -P ./libmsp430.so.zip https://github.com/kyleparrott/libmsp430/blob/master/libmsp430.so.zip?raw=true
unzip libmsp430.so.zip
mv libmsp430.so /usr/lib
rm libmsp430.so.zip

#do the pip setup and installation things
pip install --upgrade pip
pip install kubos-cli

kubos update
mv ~/.kubos /home/ubuntu/

#KubOS Linux setup
echo "Installing KubOS Linux Toolchain"
apt-get install -y minicom
apt-get install -y libc6-i386 lib32stdc++6 lib32z1
tar -xf /home/ubuntu/iobc_toolchain.tar.gz -C /usr/bin
mv /home/ubuntu/minirc.kubos /etc/minicom/minirc.kubos
mv /home/ubuntu/ftdi-usb.rules /etc/udev/rules.d/ftdi-usb.rules
rm /home/ubuntu/iobc_toolchain.tar.gz
echo "export PATH=/usr/bin/iobc_toolchain/usr/bin:$PATH" >> /etc/profile

echo "Finishing provisioning..."
