# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : zhengdongqi
@Email   : dongqi.zheng@mxplayer.in
@Usage   :
@FileName: 00.attachment.py
@DateTime: 2022/9/2 19:08
@SoftWare: PyCharm
"""

import os
import sys


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = CURRENT_DIR[:CURRENT_DIR.find('项目名称') + len('项目名称')]
sys.path.insert(0, PROJECT_DIR) if PROJECT_DIR not in sys.path else None