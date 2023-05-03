# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : zhengdongqi
@Email   : dongqi.zheng@mxplayer.in
@Usage   :
@FileName: 08.rgb2hsv.py
@DateTime: 2022/9/2 19:15
@SoftWare: PyCharm
"""

from logging import Formatter
import sys
import cv2
from numpy.core.fromnumeric import shape

color_dict = {
    'black': [(0, 180), (0, 255), (0, 46)],
    'gray': [(0, 180), (0, 43), (46, 220)],
    'white': [(0, 180), (0, 30), (221, 225)],
    'red': [(0, 10), (43, 255), (46, 255)],
    'red1': [(156, 180), (43, 255), (46, 255)],
    'orange': [(11, 25), (43, 255), (46, 255)],
    'yellow': [(26, 34), (43, 255), (46, 255)],
    'green': [(35, 77), (43, 255), (46, 255)],
    'cyan': [(78, 99), (43, 255), (46, 255)],
    'blue': [(100, 124), (43, 255), (46, 255)],
    'purple': [(125, 155), (43, 255), (46, 255)],
}

rate_dict = {
    'black': 0.0,
    'gray': 0.0,
    'white': 0.0,
    'red': 0.0,
    'red1': 0.0,
    'orange': 0.0,
    'yellow': 0.0,
    'green': 0.0,
    'cyan': 0.0,
    'blue': 0.0,
    'purple': 0.0,
}

def main_color(pic_name):
    read = cv2.imread(pic_name)
    rect = cv2.cvtColor(read, cv2.COLOR_BGR2HSV)
    row, col, _ = shape(rect)
    for i in range(row):
        for j in range(col):
            for (k, v) in color_dict.items():
                if (v[0][0] <= rect[i][j][0] <= v[0][1]) \
                and (v[1][0] <= rect[i][j][1] <= v[1][1]) \
                and (v[2][0] <= rect[i][j][2] <= v[2][1]):
                    rate_dict[k] += 1

    for (k, v) in rate_dict.items():
        print('{} : {}'.format(k, v / (row*col)))


if __name__ == '__main__':
    pic_name = str(sys.argv[1])
    main_color(pic_name)
