# Install rust stuff
# We do this as vagrant because it
# installs to $HOME/
# Rust toolchain + Cargo
curl https://sh.rustup.rs -sSf | sh -s -- -y
echo 'export PATH=$PATH:"~/.cargo/bin"' >> /home/vagrant/.bashrc
/home/vagrant/.cargo/bin/rustup default 1.32.0
# bbb/mbm2 target
/home/vagrant/.cargo/bin/rustup target install arm-unknown-linux-gnueabihf
# iobc target
/home/vagrant/.cargo/bin/rustup target install armv5te-unknown-linux-gnueabi
# install cargo-kubos
/home/vagrant/.cargo/bin/cargo install --git https://github.com/kubos/cargo-kubos
# setup cargo config
mv /home/vagrant/cargo_config /home/vagrant/.cargo/config
# Install file-client
/home/vagrant/.cargo/bin/cargo install --path /home/vagrant/.kubos/kubos/clients/kubos-file-client/
# Install shell-client
/home/vagrant/.cargo/bin/cargo install --path /home/vagrant/.kubos/kubos/clients/kubos-shell-client/
# Install example UART comms client
/home/vagrant/.cargo/bin/cargo install --path /home/vagrant/.kubos/kubos/clients/uart-comms-client/

# Install app-api python module
cd /home/vagrant/.kubos/kubos/apis/app-api/python && python3 -m pip install .

# Install kubos-service python module
cd /home/vagrant/.kubos/kubos/libs/kubos-service && python3 -m pip install .

echo "Finishing provisioning..."
