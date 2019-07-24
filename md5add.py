# -*- coding:utf-8 -*-
import hashlib
import os

def fileBackup(fileName):
    oldFile = open(fileName, 'r')
    newFileName = fileName[:fileName.rfind('.')] + '_backup' + fileName[fileName.rfind('.'):]
    print('正在备份文件为：%s' % newFileName)
    newFile = open(newFileName, 'w')
    for lineContent in oldFile.readlines():
        newFile.write(lineContent)
    oldFile.close()
    newFile.close()

def md5Add():

    # 获取当前python文件的绝对路径
    pwd = os.getcwd()
    # 列出给定路径下的所有文件
    fileList = os.listdir(pwd)
    # 排除当前python文件
    fileList.remove('md5add.py')
    # print(fileList)
    for i, file in enumerate(fileList):
        print('正在读取第%d个文件：%s' % (i + 1, file))
        readFile = open(file, 'rb')
        md5 = hashlib.md5(readFile.read()).hexdigest()
        readFile.close()
        print('该文件的MD5值为：%s' % md5)

        dotIndex = file.rfind('.')
        fileName = file[:dotIndex]
        fileType = file[dotIndex:]
        # print('fileName:%s, fileType:%s' % (fileName, fileType))
        newName = fileName + '-' + md5 + fileType
        os.rename(file, newName)

print("")
md5Add()
