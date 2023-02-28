import logging
from . import execute
from datetime import datetime


log = logging.getLogger(__name__)

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

def disk_partition_mbr_create(DISK_MD):

    log.info(f'Partitioning the raw disk image with MBR at  {now.strftime("%H:%M:%S")}')
    log.info(f'gpart create -s MBR {DISK_MD}')
    return execute(f'gpart create -s MBR {DISK_MD}')
