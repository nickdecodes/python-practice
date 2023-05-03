# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : zhengdongqi
@Email   : dongqi.zheng@mxplayer.in
@Usage   :
@FileName: 07.compress_pic.py
@DateTime: 2022/9/2 19:13
@SoftWare: PyCharm
"""

import os
import os.path
import click
import tinify
import sys

tinify.key = "VmRQ2PFqH4nW2lhWzvh5mK895w0L2pKh"
targetFileDirName = "/compress"  # 输出目录
targetIsDir = False
totalPicCount = 1  # 压缩图片总数
compressSuccessPicCount = 0  # 图片压缩成功的数量


# 这里就是通过tingPng压缩图片的核心代码
def compress_core(file, outputFile):
    source = tinify.from_file(file)  # 压缩指定文件
    source.to_file(outputFile)  # 将压缩后的文件输出当指定位置


def compress_file(file):
    if not os.path.isfile(file):
        print("你指定的不是文件,不给你压缩这个文件!")
        return
    srcFiledirName = os.path.dirname(file)
    basename = os.path.basename(file)  # 获得文件全称 例如  migo.png
    filename, fileSuffix = os.path.splitext(basename)  # 获得文件名称和后缀名  例如 migo 和 png
    if picIsCorrect(fileSuffix):
        targetFileDir = srcFiledirName + targetFileDirName
        if not os.path.isdir(targetFileDir):
            os.mkdir(targetFileDir)
        print("正在压缩的图片:  %s" % (srcFiledirName + "/" + basename))
        compress_core(file, targetFileDir + "/" + basename)
        global compressSuccessPicCount
        compressSuccessPicCount += 1
        global targetIsDir
        if targetIsDir is not True:
            print("------------压缩的图片在:  %s  目录下" % (targetFileDir))
    else:
        print("暂不支持压缩 {} 格式的文件, 文件名: {}".format(fileSuffix, basename))


def picIsCorrect(fileSuffix):
    if fileSuffix == ".png" or fileSuffix == ".jpg" or fileSuffix == ".jpeg":
        return True
    else:
        return False


def compress_dir(dir):
    if not os.path.isdir(dir):
        print("你输入的不是一个目录")
        return
    else:
        global targetIsDir
        targetIsDir = True
        srcFilePath = dir  # 源路径
        for root, dirs, files in os.walk(srcFilePath):
            global totalPicCount
            totalPicCount = len(files)
            for name in files:
                compress_file(srcFilePath + "/" + name)
            break  # 仅遍历当前目录
    print("------------所有压缩的图片都在: %s  目录下" % (srcFilePath + targetFileDirName))


@click.command()
@click.option('-f', "--file", type=str, default=None, help="单个文件压缩")
@click.option('-d', "--dir", type=str, default=None, help="被压缩的文件夹")
def run(file, dir):
    if not file is None:
        compress_file(file)  # 压缩指定的文件
        pass
    elif not dir is None:
        compress_dir(dir)  # 压缩指定的目录
        pass
    else:
        compress_dir(os.getcwd())  # 压缩当前文件夹
        print("当前目录: %s" % (os.getcwd()))
    print("------压缩结束!------图片总数 ({}),  压缩的图片数量 ({})".format(totalPicCount, compressSuccessPicCount))


if __name__ == "__main__":
    # run()
    file_path = str(sys.argv[1])
    compress_file(file_path)
