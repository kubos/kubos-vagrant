#!/bin/bash
#README: This script only checks for programs to be installed and accessible in the default PATH.
#To add more programs to check for add them to the programs array.

red='\E[31m'
green='\E[32m'

programs=(
    cmake
    lsusb
    python
    python3
)

test_installed () {
    if command -v $1 > /dev/null
    then
        printf "$green$1 => found\n"
    else
        printf "$red$1 => not found\n" >&2
    fi
    tput sgr0 #reset to normal text output
}

for prog in "${programs[@]}"
do
    test_installed $prog
done
