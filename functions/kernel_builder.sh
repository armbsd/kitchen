
function kernel_build_all () {

#
# Get path to SRC tree
#
if [ -z "$1" ]; then
  echo "Usage: $0 path-to-svn-src-tree"
  exit 1
fi

if [ ! -d "$1" ]; then
  echo "Error: Provided path ($1) is not a directory"
  exit 1
fi

export SRC=$(realpath $1)
export MAKESYSPATH=$SRC/share/mk
if [ ! -d "$MAKESYSPATH" ]; then
  echo "Error: Can't find svn src tree"
  exit 1
fi

#
# Create dirs
#
mkdir -p $ROOTFS $MAKEOBJDIRPREFIX
#
# Number of CPU for parallel build
#
export NCPU=$(sysctl -n hw.ncpu)
#
# Build FreeBSD
#

echo "Building kernel"
cd $SRC && \
make -j $NCPU buildkernel KERNCONF=GENERIC || exit $?

#
# Install FreeBSD
#

echo "Installing kernel"
cd $SRC && \
make -DNO_ROOT DESTDIR=$ROOTFS installkernel KERNCONF=GENERIC || exit $?


echo "Kernel installed!"

}
