Buuild logs of the croched 

```sh

root@freebsd:~/crochet # sh crochet.sh -b RaspberryPi3
Starting at Tue Feb 28 18:19:57 UTC 2023
Board: RaspberryPi3
Source version is: 7d1f66652
Building FreeBSD version: 12.4
Image name is:
    /root/crochet/work/FreeBSD-aarch64-12.4-GENERIC-7d1f66652-RaspberryPi3.img
Building FreeBSD version: 12.4
[Creating objdir /root/crochet/work/obj/usr/src/amd64.amd64...]
[Creating objdir /root/crochet/work/obj/usr/src/arm64.aarch64...]
Object files are at: /root/crochet/work/obj/usr/src
Found suitable FreeBSD source tree in:
    /usr/src
Please install u-boot-rpi3 and re-run this script.
You can do this with:
  $ sudo pkg install u-boot-rpi3
or by building the port:
  $ cd /usr/ports/sysutils/u-boot-rpi3
  $ make -DBATCH all install



  root@freebsd:~/crochet # sh crochet.sh -b RaspberryPi3
Starting at Tue Feb 28 18:21:08 UTC 2023
Board: RaspberryPi3
Source version is: 7d1f66652
Building FreeBSD version: 12.4
Image name is:
    /root/crochet/work/FreeBSD-aarch64-12.4-GENERIC-7d1f66652-RaspberryPi3.img
Building FreeBSD version: 12.4
Object files are at: /root/crochet/work/obj/usr/src
Found suitable FreeBSD source tree in:
    /usr/src
Found U-Boot port in:
    /usr/local/share/u-boot/u-boot-rpi3
Please install sysutils/rpi-firmware and re-run this script.
You can do this with:
  $ sudo pkg install sysutils/rpi-firmware
or by building the port:
  $ cd /usr/ports/sysutils/rpi-firmware
  $ make -DBATCH all install



root@freebsd:~/crochet # pkg install sysutils/rpi-firmware
Updating FreeBSD repository catalogue...
FreeBSD repository is up to date.
All repositories are up to date.
The following 1 package(s) will be affected (of 0 checked):

New packages to be INSTALLED:
        rpi-firmware: 1.20210303.g20210303

Number of packages to be installed: 1

The process will require 22 MiB more space.
4 MiB to be downloaded.

Proceed with this action? [y/N]: y
[1/1] Fetching rpi-firmware-1.20210303.g20210303.pkg: 100%    4 MiB   4.6MB/s    00:01    
Checking integrity... done (0 conflicting)
[1/1] Installing rpi-firmware-1.20210303.g20210303...
[1/1] Extracting rpi-firmware-1.20210303.g20210303: 100%
=====
Message from rpi-firmware-1.20210303.g20210303:

--
The rpi-firmware package installs files to /usr/local/share/rpi-firmware/.
To update the firmware used to boot, copy these files to /boot/msdos,
and then copy the appropriate config_<type>.txt file to
/boot/msdos/config.txt.

For example, on a Raspberry Pi 4 Model B,

  cp -pr /usr/local/share/rpi-firmware/* /boot/msdos/
  cp /boot/msdos/config_rpi4.txt /boot/msdos/config.txt
```