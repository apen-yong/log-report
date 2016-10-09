#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by follow on 2016/9/28

from utils.excel_tools import Report


if __name__ == '__main__':
    r = Report(file_name="my_report.xls", log_path="/Users/yongzhou/access_20160925.log")
    r.insert_detail_info()
    r.insert_chart()
    r.close_workbook()
