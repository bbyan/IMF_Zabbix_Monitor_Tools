# coding:utf-8
import os
import logging
import re
from datetime import datetime

fmt = '%(asctime)s %(levelname)s %(module)s %(message)s'
dateFmt = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(level=logging.INFO, format=fmt, datefmt=dateFmt, filename='/var/log/analyze/afds_analysis.log',
                    filemode='aw')


def run_curl():
    cmd = 'curl -u lubin:57336969 -k "sftp://127.0.0.1/mnt/c/Users/bbyan/afds_aims.log"  -r -512000 -s'
    #cmd = 'curl -u ibuser:57336969 -k "sftp://10.211.55.101/home/ibuser/afds_aims.log"  -r -512000 -s'
    #cmd = 'curl --noproxy "*" -u nginx: --pubkey /Users/lubin/.ssh/id_rsa.pub ' \
    #      '--key /Users/lubin/.ssh/id_rsa -k "sftp://10.99.1.130/home/nginx/afds_aims.log"  -r -512000 -s'
    returnlist = os.popen(cmd).readlines()
    return returnlist


def process_list(loglist):
    pattern = re.compile(ur'\d{4}\-\d{2}\-\d{2}\s\d{2}:\d{2}:\d{2}')
    logging.debug(loglist)
    loglist.reverse()
    logging.debug('reversed %s', loglist)
    for line in loglist:
        index = line.find('Origin Date is: ')
        if index != -1:
            logging.debug(index)
            logging.debug(line)
            logging.debug(type(line))
            logging.debug(pattern.search(line[index:]).group())
            f_last_afds_occur_time = datetime.strptime(
                pattern.search(line[index:]).group(), '%Y-%m-%d %H:%M:%S')
            logging.debug(type(f_last_afds_occur_time))
            return f_last_afds_occur_time


if __name__ == '__main__':
    logging.info('------The script run started.------')
    lists = run_curl()
    last_afds_occur_time = process_list(lists)
    system_date_time = datetime.now()
    logging.debug(type(system_date_time))
    logging.debug(type(last_afds_occur_time))
    logging.info('The system date time is                   : ' + system_date_time.__str__())
    logging.info('The afds service last occur time is       : ' + last_afds_occur_time.__str__())
    time_difference = (system_date_time - last_afds_occur_time).seconds / 60
    logging.info('The difference between the two times is   : ' + time_difference.__str__())

    if time_difference <= 10:
        print('1')
        logging.info('The status is                             : 1')
    else:
        print('0')
        logging.info('The status is                             : 0')
    logging.info('------The script run end.------\n')
