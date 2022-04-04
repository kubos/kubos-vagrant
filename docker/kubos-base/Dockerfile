FROM ubuntu:18.04

LABEL org.opencontainers.image.authors="catherine@kubos.com, ryan@kubos.com" \
	version="1.20.1" \
	com.example.vendor="The KubOS Community"

RUN apt-get update -y

RUN apt-get upgrade --no-install-recommends -y python3.7
RUN apt-get install --no-install-recommends -y pkg-config build-essential git cmake unzip wget sqlite3 libsqlite3-dev libssl-dev curl ssh

# Linux build dependencies
RUN apt-get install --no-install-recommends -y python file rsync bc cpio ncurses-dev libc6-i386 lib32stdc++6 lib32z1

#Tools to generate docs
RUN apt-get install --no-install-recommends -y doxygen graphviz plantuml

# resolvconf is no longer included by default as of Ubuntu 18.04
# apt-get install -y resolvconf
# rm -f /etc/resolv.conf
# # There's something wrong with the default resolv.conf symlink. This fixes it
# ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf


# Install pip for Python2 and Python3
RUN apt-get install --no-install-recommends -y python3-pip python3-setuptools

# So that we have bdist_wheel available when installing other packages
RUN pip3 install wheel

#Kubos Linux setup
RUN echo "Installing Kubos Linux Toolchain"

RUN wget https://s3.amazonaws.com/kubos-world-readable-assets/iobc_toolchain.tar.gz && tar -xf ./iobc_toolchain.tar.gz -C /usr/bin && rm ./iobc_toolchain.tar.gz

RUN wget https://s3.amazonaws.com/kubos-world-readable-assets/bbb_toolchain.tar.gz && tar -xf ./bbb_toolchain.tar.gz -C /usr/bin && rm ./bbb_toolchain.tar.gz

# Install NOS3 dependencies
RUN apt-get --no-install-recommends install -y software-properties-common
# This was originally a cz.archive domain not us.
RUN add-apt-repository 'deb http://us.archive.ubuntu.com/ubuntu xenial main universe'
RUN apt-get install -y libboost-system1.58.0 libboost-program-options1.58.0 libxerces-c3.1
RUN wget https://github.com/nasa/nos3/raw/v1_04_00/support/packages/ubuntu/itc-common-cxx11-Release_1.9.1_amd64.deb && \
apt-get install -y ./itc-common-cxx11-Release_1.9.1_amd64.deb && rm itc-common-cxx11-Release_1.9.1_amd64.deb

RUN wget https://github.com/nasa/nos3/raw/v1_04_00/support/packages/ubuntu/nos-engine-cxx11-Release_1.4.0_amd64.deb && \
apt-get install -y ./nos-engine-cxx11-Release_1.4.0_amd64.deb && rm nos-engine-cxx11-Release_1.4.0_amd64.deb

ENV PATH "$PATH:/usr/bin/iobc_toolchain/usr/bin:/usr/bin/bbb_toolchain/usr/bin"
