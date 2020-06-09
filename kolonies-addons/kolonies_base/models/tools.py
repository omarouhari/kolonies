# -*- coding: utf-8 -*-

import hashlib
from datetime import time


def convert_float_to_time(time_float=0.0):
    time_format = '{0:02.0f}:{1:02.0f}'.format(*divmod(float(time_float) * 60, 60))
    hour = int(time_format.split(':')[0])
    minute = int(time_format.split(':')[1])
    return time(hour, minute)


def hash_string_hex(string_to_hash=False):
    if not string_to_hash:
        return False
    if not isinstance(string_to_hash, str):
        return False
    hash_object = hashlib.sha1(string_to_hash.encode('utf-8'))
    return hash_object.hexdigest()
