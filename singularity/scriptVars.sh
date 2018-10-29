EFFECTIVE_GO_PATH="$(go env | grep GOPATH | cut -d= -f2 | tr -d '"')"
EFFECTIVE_GO_BIN_PATH="$EFFECTIVE_GO_PATH/bin"
SINGULARITY_SOURCE_DIR="$EFFECTIVE_GO_PATH/src/github.com/sylabs/singularity"
SINGULARITY_INSTALL_LOG_FILE="$SINGULARITY_SOURCE_DIR/installationLog.txt"
BASHRC_SIGNATURE=d80aeab9ea6de86f5004d9acdb481c50

politeSetValue(){
  local HELP_TEXT="$1"
  local DEFAULT="$2"
  shift 2
  local VALID_VALUE="false"
  local RESP=""
  local OPTIONS="$DEFAULT"
  for opt in "$@" ; do
    OPTIONS="${OPTIONS}|${opt}"
  done

  while ! $VALID_VALUE ; do
    >&2 echo -ne "$HELP_TEXT (${OPTIONS})(default: $DEFAULT) "
    read RESP
    if [ -z "$RESP" ] ; then
      RESP="$DEFAULT"
      VALID_VALUE='true'
    fi
    for opt in $DEFAULT "$@" ; do
      [ "$RESP" = "$opt" ] &&  VALID_VALUE="true" && break
    done
  done
  echo "$RESP"
}


errcho(){
    >&2 echo "$@"
}
