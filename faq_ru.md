### Как открыть готовый образ в системе ? 

Create a memory disk from it (man mdconfig), mount FreeBSD partition (md0s2a, probably) then copy that dtb into /mnt/boot/dtb.

### Как скачать исходники ? 

```
pkg install subversion
#Для использования метода https
pkg install ca_root_nss
rm -rf /usr/src
svn co https://svn.freebsd.org/base/head /usr/src
rm -rf /usr/doc
svn co https://svn.freebsd.org/doc/head /usr/doc
rm -rf /usr/ports
svn co https://svn.freebsd.org/ports/head /usr/ports
```
### Как скомпилировать ядро ? 
Попробуем скрипт 
```
#!/bin/sh


export TARGET=arm64

#
# Predefined path to workspace

export WORKSPACE=$PWD/arm64-workspace
export MAKEOBJDIRPREFIX=$WORKSPACE/obj/
export ROOTFS=$WORKSPACE/rootfs

#
# Sanity checks
#
if [ "$USER" == "root" ]; then
  echo "Error: Can't run under root"
  exit 1
fi

if [ "$(uname -s)" != "FreeBSD" ]; then
  echo "Error: Can run on FreeBSD only"
  exit 1
fi

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
make -j $NCPU buildkernel KERNCONF=GENERIC -DNO_MODULES || exit $?

#
# Install FreeBSD
#

echo "Installing kernel"
cd $SRC && \
make -DNO_ROOT -DWITHOUT_TESTS -DNO_MODULES DESTDIR=$ROOTFS installkernel KERNCONF=GENERIC || exit $?


echo "Kernel installed!"
```

### Как скомпилировать userland ? 

### Как запаковать мою прошику в образ диска ? 

### Как записать образ диска на флешку из под FreeBSD? 
```
dd bs=1m if=FreeBSD-12.0-CURRENT-arm64-aarch64-RPI3-20180802-r337160.img | pv | of=/dev/da0
```
или 

```
dd if=FreeBSD-12.0-CURRENT-arm64-aarch64-RPI3-20180802-r337160.img of=/dev/da0 bs=4m conv=sync
```

### Как открыть образ диска и заменить на свое ядро не повредив образ? 

```
mdconfig file
mdconfig -d -u 0
```

### Как пропатчить исходники? 

```
 cd /usr/src && patch < patchfile.
```
### Где взять свежие образы на Raspberry PI3 

Тут и исходники имеются 

```
https://download.freebsd.org/ftp/snapshots/arm64/aarch64/ISO-IMAGES/12.0/
```
tar xvfz Freebsd.img.xz

### Как отформатировать диск в FAT32

```
fdisk -BI /dev/da0
newfs_msdos /dev/da0s1
```
### Как примонтировать устроство FAT32

```
 mount -t msdosfs  /dev/da0s1 /mnt 
```
### Узнать версию репозитория SVN 

```
root@:/usr/src # svnversion
337960
```
###  Format script 

```
#!/usr/local/bin/bash
echo "Hello in the format script"
echo -n "Enter your disk: "
read disk
for i in /dev/$disk*
do
mount | grep $i
if [[ (( $? -eq '0')) ]];then 
umount $i
echo "unmount $i done!"
fi || exit $?
done
echo "Format disk!"
  fdisk -BI /dev/$disk
  newfs_msdos /dev/$disk
echo "Format done!"
```
### ARM BSD KITCHEN 

 Пункты меню 
1. Сделать ядро 
2. Сделать userlend
3. Собрать прошику. 