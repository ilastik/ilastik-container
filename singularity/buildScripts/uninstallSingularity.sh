#!/bin/bash
set -u
set -e

source installationCommon.sh

if [ -f $SINGULARITY_INSTALL_LOG_FILE ]; then
    INSTALLED_FILES="$(cat $SINGULARITY_INSTALL_LOG_FILE | grep INSTALL | grep -E -o '/[^ ]+')"

    errcho "Remove all of these files?"
    echo $INSTALLED_FILES | tr ' ' '\n' >&2
    ANSWER="$(politeSetValue "Remove files?" y n)"
    if [ $ANSWER = y ]; then
        sudo rm --preserve-root -rfv $INSTALLED_FILES
    else
        errcho "Aborting uninstall"
        exit 1
    fi
else
    if type singularity > /dev/null 2</dev/null ; then
        errcho "Could not find singularity installation log file at $SINGULARITY_INSTALL_LOG_FILE."
        errcho "but singularity seems to be installed, as it is in your PATH."
        exit 2
    else
        errcho "Singularity does not seem to be installed in your system files"
        errcho "It sould be safe to delete the source folder at $SINGULARITY_SOURCE_DIR"
    fi
fi

errcho "Removing singularity source directory at $SINGULARITY_SOURCE_DIR"
rm -rf $SINGULARITY_SOURCE_DIR

errcho "Cleaning stuff from .bashrc"
sed -i "/^.*$BASHRC_SIGNATURE/d" ~/.bashrc


errcho "Singularity successfully uninstalled"
