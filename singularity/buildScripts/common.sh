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
