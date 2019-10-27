# coding:utf-8
import os
import logging
import re
import sys
from datetime import datetime

fmt = '%(asctime)s %(levelname)s %(module)s %(message)s'
dateFmt = '%Y-%m-%d %H:%M:%S'

# logging.basicConfig(level=logging.INFO, format=fmt, datefmt=dateFmt, filename='/var/log/analyze/nginx_analysis.log',
#                    filemode='aw')

logging.basicConfig(level=logging.INFO, format=fmt, datefmt=dateFmt)


def run_curl():
    cmd = 'curl -u lubin:57336969 -k "sftp://127.0.0.1/home/lubin/access.log"  -r -512000 -s'
    returnlist = os.popen(cmd).readlines()
    return returnlist


def process_list(loglist):
    pattern = re.compile(ur'\d{4}\-\d{2}\-\d{2}\s\d{2}:\d{2}:\d{2}')
    logging.debug(loglist)
    loglist.reverse()
    logging.debug('reversed %s', loglist)
    subsystem_name = sys.argv[1]
    logging.debug(subsystem_name)
    for line in loglist:
        index = line.find(subsystem_name)
        if index != -1:
            logging.debug(index)
            logging.debug(line)
            logging.debug(type(line))
            logging.debug(pattern.search(line[index:]).group())
            f_last_subsystem_get_time = datetime.strptime(
                pattern.search(line[index:]).group(), '%Y-%m-%d %H:%M:%S')
            logging.debug(type(f_last_subsystem_get_time))
            return f_last_subsystem_get_time


if __name__ == '__main__':
    logging.info('------The script run started.------')
    lists = run_curl()
    last_subsystem_get_time = process_list(lists)
    system_date_time = datetime.now()
    logging.debug(type(system_date_time))
    logging.debug(type(last_subsystem_get_time))
    logging.info('The system date time is                   : ' + system_date_time.__str__())
    logging.info('The subsystem last get time is            : ' + last_subsystem_get_time.__str__())
    time_difference = (system_date_time - last_subsystem_get_time).seconds / 60
    logging.info('The difference between the two times is   : ' + time_difference.__str__())

    if time_difference <= 10:
        print('1')
        logging.info('The status is                             : 1')
    else:
        print('0')
        logging.info('The status is                             : 0')
    logging.info('------The script run end.------\n')
