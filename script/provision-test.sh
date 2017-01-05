#!/bin/bash

red='\E[31m'
green='\E[32m'
alias Reset="tput sgr0"

programs=( \
    "arm-none-eabi-gcc"    \
    "arm-none-eabi-gdb"    \
    "msp430-gcc"   \
    "msp430-gdb"   \
    "openocd"  \
    "mspdebug" \
    "dfu-util"  \
    )


test_installed () {
    command -v $1 > /dev/null &&  printf "$green$1  => found\n"  ||  printf "$red$1 => not found\n" fi
    Reset
}

for prog in "${programs[@]}"
do
    test_installed $prog
done
