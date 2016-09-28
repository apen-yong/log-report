#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by follow on 16/9/26

"""
 读取一个日志文件并提取日志里面的如下信息
 1: hash 请求状态（200、404）的统计
 2: 特定url的响应时间list
 3: 请求总数、来源独立ip、总请求数、
"""

import logging
import re

logger = logging.getLogger("reader")
pages = {'cart': 'MyCart\.aspx',
         'contacts': 'Contacts\d+\.html'
         }


class LogFile:
    def __init__(self, *args, **kwargs):
        regex = '([\d\.]+) - ([\d\.-]+) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)"' \
                ' "(.*?)" "(.*?)" "(.*?)"  "(.*?)" "(.*?)"'
        print "read file {}".format(args[0])
        self.fh = open(args[0], "r")
        self.all_logs = []
        self.count = 0
        for line in self.fh.readlines():
            self.count += 1
            try:
                log_regex_list = re.match(regex, line).groups()
                self.all_logs.append(log_regex_list)
            except AttributeError, e:
                # print "Not from cdn. {}".format(e)
                continue
        self.pages_server_time = {}
        for p in pages.keys():
            self.pages_server_time[p] = []

    def server_time(self):
        print "Start to proccess {} logs from file".format(self.count)
        for log in self.all_logs:
            for k in pages.keys():
                if re.search(pages.get(k), log[3]):
                    self.pages_server_time[k].append([log[2], log[8]])
                    # print  "{}: {}".format(log[2], log[8])
        return self.pages_server_time

    def status_hash(self):
        pass

    def info(self):
        pass


if __name__ == '__main__':
    mylog = LogFile("/Users/yongzhou/access_20160925.log")
    mylog.server_time()