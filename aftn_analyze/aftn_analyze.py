# !/usr/bin/python
# -*- coding: utf-8 -*-

from ftplib import FTP
from datetime import datetime
import re
import ConfigParser

#Initialize the extrenal configuration file
cf = ConfigParser.ConfigParser()
cf.read("./aftn_analyze.conf")
destPath = cf.get("serverInfo","destPath")
serverIP = cf.get("serverInfo","aftnServer")
serverAccount = cf.get("serverInfo","account")
serverPassword = cf.get("serverInfo","password")


def ftpconnect(host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)         #打开调试级别2，显示详细信息
    ftp.connect(host, 21)  # 连接
    ftp.login(username, password)  # 登录，如果匿名登录则用空串代替即可
    return ftp


def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024  # 设置缓冲块大小
    fp = open(localpath, 'wb')  # 以ls写模式在本地打开文件
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)  # 接收服务器上文件并写入本地文件
    # ftp.set_debuglevel(0)  # 关闭调试
    fp.close()  # 关闭文件


if __name__ == "__main__":
    sourceFileName = "LOG_" + datetime.now().strftime("%Y%m%d") + ".log"
    desnationFilePath = destPath + sourceFileName
    ftp = ftpconnect(serverIP, serverAccount, serverPassword)
    downloadfile(ftp, sourceFileName, desnationFilePath)
    ftp.quit()

    nCount = 0
    zcCount = 0

    fh = open(desnationFilePath)
    lines = fh.readlines()
    #lines.reverse()
    count = len(lines)
    for line in lines[-4000:]:
        if re.search(r'NNNN', line):
            nCount = nCount + 1
        if re.search(r'ZCZC', line):
            zcCount = zcCount + 1

    print abs(nCount - zcCount)
    print count