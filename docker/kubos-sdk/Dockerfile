FROM kubos-base

# Install more priviliged dependencies that only seem to be needed in the SDK environment

RUN apt-get install -y software-properties-common

# Install kernel additions for better USB device recognition
RUN apt-get install -y linux-image-extra-virtual

RUN apt-get install -y libffi-dev libhidapi-hidraw0 gdb
ninja-build python-dev libffi-dev 

RUN apt-get install -y sshpass


# Documentation tools
RUN apt-get install -y texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended latexmk texlive-fonts-extra

# KubOS Linux setup
# echo "Installing KubOS Linux Toolchains"

RUN apt-get install -y minicom

# Utilities for building KubOS Linux
RUN apt-get install -y mtools


# Copy configs
COPY ../bin/minirc.kubos /etc/minicom/minirc.kubos
COPY ../bin/kubos-usb.rules /etc/udev/rules.d/kubos-usb.rules

# Create user accounts
RUN useradd --create-home --shell /bin/bash kubos
RUN adduser kubos sudo
RUN adduser kubos dialout

RUN echo 'kubos:Kubos123' | chpasswd

#Vagrant commands may act funny without password-less sudo
RUN echo "kubos ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER kubos
WORKDIR /home/kubos

RUN mkdir -p /home/kubos/.kubos
# Install all Kubos Python dependencies

RUN git clone https://github.com/kubos/kubos /home/kubos/.kubos/kubos --depth 1 && pip3 install -r kubos/requirements.txt
#&& rm -r kubos
RUN chown -R kubos /home/kubos/.kubos

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






