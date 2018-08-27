function format_disk () {

#
# format script 
#
echo "We need sudo access"
echo "Hello in the format script"
echo -n "Enter your disk: "
read disk
for i in /dev/$disk*
do
mount | grep $i
if [[ (( $? -eq '0')) ]];then 
sudo umount $i
echo "unmount $i done!"
fi || exit $?
done
echo "Format disk!"
sudo fdisk -BI /dev/$disk
sudo newfs_msdos /dev/$disk
echo "Format done!"
}
