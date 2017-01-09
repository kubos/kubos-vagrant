#!/bin/bash
#README: This script only checks for programs to be installaed and accessible in the default PATH.
#to add more programs to check for add them to the programs.txt file in the same directory.
result=0
red='\E[31m'
green='\E[32m'

#Only intended to run inside the vagrant box Which has bash v4.x and has the readarray command
readarray programs < programs.txt

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
