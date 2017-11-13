pip install pysocks pyserial #Temporary - This will be added to the kubos-cli requirements.txt
pip install git+https://github.com/kubostech/kubos-cli
pip install cryptography==1.9

mkdir -p /usr/local/lib/yotta_modules
mkdir -p /usr/local/lib/yotta_targets
mkdir -p /home/vagrant/.kubos
chown -R vagrant /home/vagrant/.kubos
chown -R vagrant /usr/local/lib/

activate-global-python-argcomplete

echo "Finished root provisioning"
