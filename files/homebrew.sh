#!/bin/bash

USER=$1
PASS=$2

echo $PASS | sudo -S su $USER
echo '' | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

exit $?
