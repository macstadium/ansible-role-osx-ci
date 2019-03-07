#!/bin/bash

USER=$1
PASS=$2

echo $PASS | sudo -S su $USER
echo '' | ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

exit $?