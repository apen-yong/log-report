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



    def get_server_time(self):
        """
        获取在pages中定义的每个类型页面之处理时间
        :return:
        """
        print "Start to proccess {} logs from file".format(self.count)
        pages_server_time = {}
        for p in pages.keys():
            pages_server_time[p] = []
        for log in self.all_logs:
            for k in pages.keys():
                if re.search(pages.get(k), log[3]):
                    pages_server_time[k].append([log[2], log[8]])
                    # print  "{}: {}".format(log[2], log[8])
        return pages_server_time

    def get_status_hash(self):
        """
        获取http状态码 并且放入刀hash中
        :return:
        """
        http_code_hash = {}
        for log in self.all_logs:
            try:
                http_code_hash[log[4]] += 1
            except KeyError, e:
                print "Found a new http status code: {}".format(e)
                http_code_hash[log[4]] = 1
        return http_code_hash

    def get_uniq_visit(self):
        """
        获取所有独立用户的ip地址
        :return:
        """
        user_visit = []
        for log in self.all_logs:
            user_visit.append(log[2])
        return set(user_visit)

    def get_count_http(self):
        return self.count


if __name__ == '__main__':
    mylog = LogFile("/Users/yongzhou/access_20160925.log")
    mylog.server_time()
