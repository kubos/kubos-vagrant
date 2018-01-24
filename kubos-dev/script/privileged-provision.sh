pip install -r https://raw.githubusercontent.com/kubos/kubos-cli/master/requirements.txt
pip install git+https://github.com/kubos/kubos-cli

mkdir -p /usr/local/lib/yotta_modules
mkdir -p /usr/local/lib/yotta_targets
mkdir -p /home/vagrant/.kubos
chown -R vagrant /home/vagrant/.kubos
chown -R vagrant /usr/local/lib/

activate-global-python-argcomplete

echo "Finished root provisioning"
