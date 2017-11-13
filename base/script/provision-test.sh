#!/bin/bash
#README: This script only checks for programs to be installed and accessible in the default PATH.
#To add more programs to check for add them to the programs array.

red='\E[31m'
green='\E[32m'

return_code=0

#Programs to ensure are installed and in the PATH
programs=(
    arm-none-eabi-gcc
    arm-none-eabi-gdb
    /usr/bin/iobc_toolchain/usr/bin/arm-linux-gcc
    /usr/bin/bbb_toolchain/usr/bin/arm-linux-gcc
    cmake
    dfu-util
    lsusb
    msp430-gcc
    msp430-gdb
    mspdebug
    python
    openocd
)

#List of file paths to test for existence
files=(
    /usr/lib/libmsp430.so
    /etc/udev/rules.d/kubos-usb.rules
    /etc/minicom/minirc.kubos
    /etc/minicom/minirc.msp430
)

test_programs_installed () {
    if command -v $1 > /dev/null
    then
        printf "$green$1 => found\n"
    else
        printf "$red$1 => not found\n" >&2
        return_code=1
    fi
    tput sgr0 #reset to normal text output
}


test_files_exist() {
    if test -e $1
    then
        printf "$green$1 => found\n"
    else
        printf "$red$1 => not found\n" >&2
        return_code=1
    fi
}


#Test for programs
for prog in "${programs[@]}"
do
    test_programs_installed $prog
done

#Test for files
for file in "${files[@]}"
do
    test_files_exist $file
done

exit $return_code
