# -*- coding: utf-8 -*-

from datetime import time


def convert_float_to_time(time_float=0.0):
    time_format = '{0:02.0f}:{1:02.0f}'.format(*divmod(float(time_float) * 60, 60))
    hour = int(time_format.split(':')[0])
    minute = int(time_format.split(':')[1])
    return time(hour, minute)
