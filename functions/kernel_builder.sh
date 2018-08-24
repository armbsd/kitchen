
function kernel_build_all () {
set -x
#
# Get path to SRC tree
#
if [ -d "SRC" ]; then
  echo "This script could not find the folder and the source code:${SRC_DIR}
"
  exit 1
fi

if [ ! -d "$MAKESYSPATH" ]; then
  echo "Error: Can't find svn src tree"
  exit 1
fi

#
# Create dirs
#
mkdir  ${WORKSPACE}

mkdir -p ${ROOTFS} ${MAKEOBJDIRPREFIX}
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
