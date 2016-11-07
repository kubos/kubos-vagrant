apt-get update
add-apt-repository -y ppa:team-gcc-arm-embedded/ppa
add-apt-repository -y ppa:george-edison55/cmake-3.x
add-apt-repository -y ppa:git-core/ppa
add-apt-repository ppa:fkrull/deadsnakes-python2.7
apt-get update
apt-get upgrade -y python2.7
apt-get -y install build-essential libssl-dev libffi-dev libhidapi-hidraw0
apt-get install -y python-setuptools build-essential ninja-build python-dev libffi-dev libssl-dev
apt-get install --force-yes gcc-arm-embedded
apt-get -y install python-pip
apt-get -y install git
apt-get install -y cmake
apt-get install -y gcc-msp430 gdb-msp430 msp430-libc
# flash tools
apt-get install mspdebug
apt-get install dfu-util
apt-get install openocd
# download libmsp430.so
wget -P /usr/lib https://github.com/kubostech/kubos/raw/vagrant-provision/vm/lib/libmsp430.so
pip install --upgrade pip
pip install kubos-cli
kubos update
mv ~/.kubos /home/vagrant/
apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

wget -P /usr/lib https://github.com/kubostech/kubos/raw/master/vm/lib/libmsp430.so

#libjim0.76
wget http://launchpadlibrarian.net/207671794/libjim0.76_0.76-1_i386.deb
dpkg -i libjim0.76_0.76-1_i386.deb
apt-get install -f
# dfu-util
wget http://mirrors.kernel.org/ubuntu/pool/universe/d/dfu-util/dfu-util_0.9-1_i386.deb
dpkg -i dfu-util_0.9-1_i386.deb
#open-ocd
wget http://launchpadlibrarian.net/216152652/openocd_0.9.0-1build1_i386.deb
dpkg -i openocd_0.9.0-1build1_i386.deb
apt-get install -f

TI_MSPGCC_URL=http://software-dl.ti.com/msp430/msp430_public_sw/mcu/msp430/MSPGCC/3_02_02_00/exports/msp430-gcc-full-linux-installer-3.2.2.0.run
TI_MSPGCC_DIR=/opt/ti-mspgcc

wget -qO installer $TI_MSPGCC_URL
echo "Installing TI MSPGCC"
chmod +x installer
./installer --mode unattended --prefix $TI_MSPGCC_DIR
# Copy headers and ldscripts to the correct location to prevent the need to explicitly include them
cp $TI_MSPGCC_DIR/{include/*.h,msp430-elf/include}
cp $TI_MSPGCC_DIR/{include/*.ld,msp430-elf/lib}

echo "export PATH=$TI_MSPGCC_DIR/bin:$PATH" >> /etc/profile
$TI_MSPGCC_DIR/install_scripts/msp430uif_install.sh

apt-get -y dist-upgrade
apt-get install -y mspdebug linux-image-extra-virtual
ln -s $TI_MSPGCC_DIR/bin/libmsp430.so /usr/lib/
apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
