source common.sh

if ! type go 2>/dev/null 1>/dev/null ; then
  errcho "ERROR: This script depends on the 'go' executable to determine singularity's installation directory"
  exit 1
fi

EFFECTIVE_GO_PATH="$(go env | grep GOPATH | cut -d= -f2 | tr -d '"')"
EFFECTIVE_GO_BIN_PATH="$EFFECTIVE_GO_PATH/bin"
SINGULARITY_SOURCE_DIR="$EFFECTIVE_GO_PATH/src/github.com/sylabs/singularity"
SINGULARITY_INSTALL_LOG_FILE="$SINGULARITY_SOURCE_DIR/installationLog.txt"
BASHRC_SIGNATURE=d80aeab9ea6de86f5004d9acdb481c50
