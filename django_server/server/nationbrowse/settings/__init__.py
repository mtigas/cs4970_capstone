import socket

hostname = socket.gethostname().replace('.', '_').lower()
try:
    custom_settings = __import__(hostname,globals(),locals(),level=1)
    __all__ = [custom_settings]
except ImportError:
    raise
    from default import *
