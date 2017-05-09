kubos update --latest || true #Can't run as root or else yotta symlinks are created to /root/.kubos/...

kubos update --tab-completion

echo "source /home/vagrant/.kubos/completion/kubos_completion" >> /home/vagrant/.bashrc

echo "Finishing provisioning..."
