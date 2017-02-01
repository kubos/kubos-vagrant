pip install pysocks #Temporary - This will be added to the kubos-cli requirements.txt
pip install kubos-cli

mkdir -p /usr/local/lib/yotta_modules
mkdir -p /usr/local/lib/yotta_targets
mkdir -p /home/vagrant/.kubos
chown -R vagrant /home/vagrant/.kubos
chown -R vagrant /usr/local/lib/yotta_modules
chown -R vagrant /usr/local/lib/yotta_targets

echo "Finished root provisioning"
