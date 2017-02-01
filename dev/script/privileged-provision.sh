pip install pysocks #Temporary - This will be added to the kubos-cli requirements.txt
pip install kubos-cli


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
chmod a+rw /dev/FTDI

mkdir -p /usr/local/lib/yotta_modules
mkdir -p /usr/local/lib/yotta_targets
mkdir -p /home/vagrant/.kubos
chown -R vagrant /home/vagrant/.kubos
chown -R vagrant /usr/local/lib/yotta_modules
chown -R vagrant /usr/local/lib/yotta_targets

echo "Finished root provisioning"
