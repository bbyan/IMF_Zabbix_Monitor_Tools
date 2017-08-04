# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: Lu Bin
Contact:blu@cm-topsci.com
"""
from ftplib import FTP
from datetime import datetime
import re
import ConfigParser


def import_config(path):
    # Initialize the extrenal configuration file
    cf = ConfigParser.ConfigParser()
    cf.read(path)
    destination_path = cf.get("serverInfo", "destination_path")
    server_ip = cf.get("serverInfo", "aftn_server")
    server_account = cf.get("serverInfo", "account")
    server_password = cf.get("serverInfo", "password")
    return destination_path, server_ip, server_account, server_password


def ftp_connect(host, username, password):
    ftp_info = FTP()
    ftp_info.connect(host, 21)
    ftp_info.login(username, password)
    return ftp_info


def download_file(ftp, remotepath, localpath):
    bufsize = 1024  # Set the buffer block size
    # Receive the file on the server and write it to the local file
    with open(localpath, 'wb') as file_object:
        ftp.retrbinary('RETR ' + remotepath, file_object.write, bufsize)


def analyze_aftn_message(destination_file_path):
    """
    By comparing the file at the end of 4000 aftn message,
    to determine whether the message is complete,
    under normal circumstances, the deviation is 1 or 0

    """
    n_count = 0
    zc_count = 0
    with open(destination_file_path) as file_object:
        lines = file_object.readlines()
        for line in lines[-4000:]:
            if re.search(r'NNNN', line):
                n_count = n_count + 1
            if re.search(r'ZCZC', line):
                zc_count = zc_count + 1
        return abs(n_count - zc_count)


if __name__ == "__main__":
    # Set the initial variable
    destination_path, server_ip, server_account, server_password = import_config("./aftn_analyze.conf")
    source_file_name = "LOG_" + datetime.now().strftime("%Y%m%d") + ".log"
    destination_file_path = destination_path + source_file_name
    # Connect and download the file
    ftp = ftp_connect(server_ip, server_account, server_password)
    download_file(ftp, source_file_name, destination_file_path)
    ftp.quit()
    # Analyze and return the processing results
    count_number = analyze_aftn_message(destination_file_path)
    print count_number
