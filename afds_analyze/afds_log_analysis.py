# coding:utf-8
import os
import logging
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO)


def run_curl():
    cmd = 'curl -u ibuser:57336969 -k "sftp://10.211.55.101/home/ibuser/afds_aims.log"  -r -512000 -s'
    returnlist = os.popen(cmd).readlines()
    return returnlist


def process_list(loglist):
    pattern = re.compile(ur'\d{4}\-\d{2}\-\d{2}\s\d{2}:\d{2}:\d{2}')
    logging.debug(loglist)
    loglist.reverse()
    logging.debug('reversed %s',loglist)
    for line in loglist:
        index = line.find('Origin Date is: ')
        if index != -1:
            logging.debug(index)
            logging.debug(line)
            logging.debug(type(line))
            logging.debug(pattern.search(line[index:]).group())
            f_last_afds_occur_time = datetime.strptime(
                pattern.search(line[index:]).group(),'%Y-%m-%d %H:%M:%S')
            logging.debug(type(f_last_afds_occur_time))
            return f_last_afds_occur_time


if __name__ == '__main__':
    lists = run_curl()
    last_afds_occur_time = process_list(lists)
    system_date_time = datetime.now()
    logging.info(type(system_date_time))
    logging.info(type(last_afds_occur_time))
    logging.info(system_date_time)
    logging.info(last_afds_occur_time)
    time_difference = (system_date_time-last_afds_occur_time).seconds / 60
    logging.info(time_difference)

    if time_difference >= 3:
        print('1')
    else:
        print('0')

