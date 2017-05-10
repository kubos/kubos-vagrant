pip install pysocks #Temporary - This will be added to the kubos-cli requirements.txt
pip install git+https://github.com/kubostech/kubos-cli

mkdir -p /usr/local/lib/yotta_modules
mkdir -p /usr/local/lib/yotta_targets
mkdir -p /home/vagrant/.kubos
chown -R vagrant /home/vagrant/.kubos
chown -R vagrant /usr/local/lib/

activate-global-python-argcomplete

echo "Finished root provisioning"
