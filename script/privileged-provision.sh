#These start an interactive prompt - I can't figure out how to fix it yet...
sudo apt-mark hold grub-common grub-pc grub-pc-bin grub2-common

apt-get update
yes | apt-get -y dist-upgrade
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

#Since this is a private repo the url is unavailable without authentication. An alternate temporary solution is on lines #31-35
# download libmsp430.so
#wget -P /usr/lib https://github.com/kubostech/kubos/raw/vagrant-provision/vm/lib/libmsp430.so

#Temporary fix for private repo hosting the libmsp430.so binary
apt-get install unzip
wget -P ./libmsp430.so.zip https://github.com/kyleparrott/libmsp430/blob/master/libmsp430.so.zip?raw=true
unzip libmsp430.so.zip
mv libmsp430.so /usr/lib
rm -rf libmsp430.so.zip

#do the pip setup and installation things
easy_install pip
pip install --upgrade pip
pip install pysocks #Temporary - This will be added to the kubos-cli requirements.txt
pip install kubos-cli


#Change the ssh key to the default vagrant insecure key so others can ssh in when they start this box locally
echo " Changing SSH keys"
echo "AuthorizedKeysFile %h/.ssh/authorized_keys" >> /etc/ssh/sshd_config
echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key" > /home/vagrant/.ssh/authorized_keysmod 0600 /home/vagrant/.ssh/authorized_keys

chmod 0600 /home/vagrant/.ssh/authorized_keys
chmod 0700 /home/vagrant/.ssh
chown -R vagrant  /home/vagrant/.ssh

#Vagrant commands may act funny without password-less sudo
echo "vagrant ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

#KubOS Linux setup
echo "Installing KubOS Linux Toolchain"

apt-get install -y minicom
apt-get install -y libc6-i386 lib32stdc++6 lib32z1

tar -xf /home/vagrant/iobc_toolchain.tar.gz -C /usr/bin
rm /home/vagrant/iobc_toolchain.tar.gz
mv /home/vagrant/minirc.kubos /etc/minicom/minirc.kubos
mv /home/vagrant/ftdi-usb.rules /etc/udev/rules.d/ftdi-usb.rules
echo "export PATH=/usr/bin/iobc_toolchain/usr/bin:$PATH" >> /etc/profile

mkdir -p /usr/local/lib/yotta_modules
mkdir -p /usr/local/lib/yotta_targets
mkdir -p /home/vagrant/.kubos
chown -R vagrant /home/vagrant/.kubos
chown -R vagrant /usr/local/lib/yotta_modules
chown -R vagrant /usr/local/lib/yotta_targets

echo "Finished root provisioning"
