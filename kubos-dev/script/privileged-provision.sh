python3 -m pip install flask
python3 -m pip install flask_graphql
python3 -m pip install graphene
python3 -m pip install mock
python3 -m pip install toml
python3 -m pip install responses

mkdir -p /home/vagrant/.kubos
git clone https://github.com/kubos/kubos /home/vagrant/.kubos/kubos
chown -R vagrant /home/vagrant/.kubos

echo "Finished root provisioning"
