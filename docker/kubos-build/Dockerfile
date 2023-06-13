FROM kubos-base

# Install all Kubos Python dependencies
RUN git clone https://github.com/kubos/kubos --depth 1 && pip3 install -r kubos/requirements.txt && rm -r kubos

# Setup rust stuff
ENV PATH "$PATH:/root/.cargo/bin"
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y && rustup toolchain uninstall stable-x86_64-unknown-linux-gnu
RUN rustup default 1.39.0 && rm -rf /root/.rustup/toolchains/*/share/doc
RUN rustup target install arm-unknown-linux-gnueabihf
RUN rustup target install armv5te-unknown-linux-gnueabi
RUN rustup component add clippy
RUN rustup component add rustfmt
RUN /root/.cargo/bin/cargo install --git https://github.com/kubos/cargo-kubos
COPY ../bin/cargo_config /root/.cargo/config
