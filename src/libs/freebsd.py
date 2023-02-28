import logging
from .executor import execute

log = logging.getLogger(__name__)

def freebsd_src_version( ):
    FREEBSD_VERSION =  "FreeBSD12-STABLE"
    log.debug(f"Building FreeBSD version: {FREEBSD_VERSION}")
    return FREEBSD_VERSION