#!/bin/bash
#README: This script only checks for programs to be installed and accessible in the default PATH.
#To add more programs to check for add them to the programs array.
#Also runs standard CI tests to check if dev dependencies are installed and available

set -ex

red='\E[31m'
green='\E[32m'

programs=(
    /usr/bin/iobc_toolchain/usr/bin/arm-linux-gcc
    /usr/bin/bbb_toolchain/usr/bin/arm-linux-gcc
    cmake
    lsusb
    python
    python3
    kubos-file-client
    kubos-shell-client
    uart-comms-client
)

#List of file paths to test for existence
files=(
    /etc/udev/rules.d/kubos-usb.rules
    /etc/minicom/minirc.kubos
)

test_files_exist() {
    if test -e $1
    then
        printf "$green$1 => found\n"
    else
        printf "$red$1 => not found\n" >&2
        return_code=1
    fi
}

test_installed () {
    if command -v $1 > /dev/null
    then
        printf "$green$1 => found\n"
    else
        printf "$red$1 => not found\n" >&2
    fi
    tput sgr0 #reset to normal text output
}

# Test for programs
for prog in "${programs[@]}"
do
    test_installed $prog
done

# Test for files
for file in "${files[@]}"
do
    test_files_exist $file
done

# Run source level tests for basic sanity
git clone https://github.com/kubos/kubos --depth 1
cd kubos

/home/vagrant/.cargo/bin/cargo test
python3 tools/ci_c.py
python3 hal/python-hal/i2c/test_i2c.py
cd apis/pumpkin-mcu-api; python3 test_mcu_api.py; cd ../..
cd apis/app-api/python; python3 test_app_api.py; cd ../../..

cd ..
rm -rf kubos
