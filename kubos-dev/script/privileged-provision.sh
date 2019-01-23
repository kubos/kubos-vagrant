pip install pyOCD==0.12.0
pip install -r https://raw.githubusercontent.com/kubos/kubos-cli/master/requirements.txt
pip install git+https://github.com/kubos/kubos-cli
pip install idna==2.6
pip install toml
pip install graphene

mkdir -p /usr/local/lib/yotta_modules
mkdir -p /usr/local/lib/yotta_targets
mkdir -p /home/vagrant/.kubos
git clone https://github.com/kubos/kubos /home/vagrant/.kubos/kubos
chown -R vagrant /home/vagrant/.kubos
chown -R vagrant /usr/local/lib/

activate-global-python-argcomplete

echo "Finished root provisioning"
