#Temporary provisioning manual installation of the kubos-cli
git clone https://github.com/kubostech/kubos-cli -b cli-wrap-up
cd kubos-cli
sudo pip uninstall kubos-cli
sudo pip install -e .

kubos update || true #Can't run as root or else yotta symlinks are created to /root/.kubos/...

echo "Finishing provisioning..."
