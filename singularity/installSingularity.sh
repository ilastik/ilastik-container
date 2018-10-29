#!/bin/bash

set -e
set -u

if ! grep -i -q -e debian /etc/os-release ; then
    >&2 echo "This script only works for debian derivatives (e.g. debian/ubuntu/mint)"
    >&2 echo "Please feel free to impelement the equivalent for other distros"
    exit 1
fi


sudo apt-get update && sudo apt-get install -y \
    build-essential \
    libssl-dev \
    uuid-dev \
    libgpgme11-dev \
    squashfs-tools \
    golang


#This here is distro-agnostic. It's just the apt stuff that is not portable

source scriptVars.sh

echo "~~>Installing go's dependency manager into $EFFECTIVE_GO_PATH"
go get -u -v github.com/golang/dep/cmd/dep

echo "~~>Building singularity needs to have some go executables in the PATH."
echo "-->Adding $EFFECTIVE_GO_BIN_PATH to your PATH in this session"
export PATH="$PATH:$EFFECTIVE_GO_BIN_PATH"

ANSWER="$(politeSetValue "Do you want to add $EFFECTIVE_GO_BIN_PATH to your PATH by editing .bashrc?" y n)"
if [ $ANSWER = y ]; then
    echo "~~>Adding stuff to your .bashrc..."
    cat  >> ~/.bashrc <<EOF
export PATH="\$PATH:$EFFECTIVE_GO_BIN_PATH" #Added automatically by installSingularity.sh $BASHRC_SIGNATURE
EOF

fi


echo "~~>Cloning Singularity source..."
mkdir -p $SINGULARITY_SOURCE_DIR
cd $SINGULARITY_SOURCE_DIR
git clone https://github.com/sylabs/singularity.git .

echo "~~>Building singularity..."
./mconfig
make -C builddir


echo "~~>Build done."
echo "~~>Time to install singularity into your system."

sudo make -C builddir install | tee $SINGULARITY_INSTALL_LOG_FILE
echo "~~>Done. You should now be able to call 'singularity' from the cmd line"
