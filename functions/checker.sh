function system_check() {

#
# checks
#
if [ "$USER" == "root" ]; then
  echo "Error: Can't run under root"
  exit 1
fi

if [ "$(uname -s)" != "FreeBSD" ]; then
  echo "Error: Can run on FreeBSD only"
  exit 1
fi
}
