#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by follow on 16/9/22


"""
新建一个excel，并且提供绘制图像的功能
"""
from datetime import time as dtime
import xlsxwriter
import time
from log_reader import LogFile


class Report:
    def __init__(self, *args, **kwargs):
        self.workbook = xlsxwriter.Workbook(kwargs.get('file_name'))
        self.worksheet = self.workbook.add_worksheet()

        self.date_format = self.workbook.add_format({'num_format': 'hh:mm:ss'})
        self.number_format = self.workbook.add_format()
        self.number_format.set_num_format('0.000')

        # Widen the first column to display the dates.
        self.worksheet.set_column('A:A', 10)

        log = LogFile(kwargs.get('log_path'))
        self.server_times = log.get_server_time()
        self.uniq_visit = log.get_uniq_visit()
        self.status_code = log.get_status_hash()
        self.count = log.get_count_http()
        self.chart_pos = 2
        self.info_pos = 2

    def insert_chart(self):
        for k in self.server_times.keys():
            print "Start to insert chart for {}".format(k)
            dates = []
            values = []
            logs_count = 0
            # The default chart width x height is 480 x 288 pixels.
            chart = self.workbook.add_chart({'type': 'line'})
            chart.set_size({'x_scale': 1.3, 'y_scale': 0.8})
            datasheet = self.workbook.add_worksheet(k)
            for log in self.server_times[k]:
                logs_count += 1
                date_from_log = time.strptime(log[0], "%d/%b/%Y:%H:%M:%S +0800")
                dates.append(dtime(date_from_log.tm_hour, date_from_log.tm_min, date_from_log.tm_sec))
                values.append(float(log[1]))

            # Write the date to the worksheet.
            datasheet.write_column('A1', dates, self.date_format)
            datasheet.write_column('B1', values, self.number_format)

            # Add a series to the chart.
            chart.add_series({
                'categories': '={}!$A$1:$A${}'.format(k, logs_count),
                'values': '={}!$B$1:$B${}'.format(k, logs_count),
            })

            # Configure the X axis as a Date axis and set the max and min limits.
            chart.set_title({
                'name': u'访问{}的源站的响应时间分布'.format(k),
                'name_font': {
                    'size': 11,
                },
            })

            chart.set_x_axis({
                'name': u'24小时时间轴',
                # 'date_axis': True,    #在windows系统中加入这个会导致错误
                'min': dtime(0, 0, 0),
                'max': dtime(23, 59, 59),
            })

            chart.set_y_axis({
                'name': u'IIS+DB 响应时间',
            })

            # Turn off the legend.
            chart.set_legend({
                'none': True,
                'layout': {
                    'x': 0.80,
                    'y': 0.37,
                    'width': 0.82,
                    'height': 0.25,
                }
            })

            # Insert the chart into the worksheet.
            self.worksheet.insert_chart('E{}'.format(self.chart_pos), chart)
            self.chart_pos += 20

    def close_workbook(self):
        self.workbook.close()

    def get_pos(self):
        p = "A{}".format(self.info_pos + 1)
        print "Write data for {}".format(p)
        self.info_pos += 1
        return p

    def insert_detail_info(self):
        table = self.worksheet.add_table('A2:C20')
        self.worksheet.set_column('A:A', 20)
        self.worksheet.set_column('C:C', 30)
        self.worksheet.write_row(self.get_pos(), [u'独立IP:', len(self.uniq_visit)])
        self.worksheet.write_row(self.get_pos(), [u'http请求总数:', self.count])
        for (code, times) in self.status_code.items():
            if code == '500':
                self.worksheet.write_row(self.get_pos(), [u"HTTP状态码 {}:".format(code), times, u"服务器返回了错误，一般是iis报错"])
            elif code == '404':
                self.worksheet.write_row(self.get_pos(), [u"HTTP状态码 {}:".format(code), times, u"资源不存在"])
            else:
                self.worksheet.write_row(self.get_pos(), [u"HTTP状态码 {}:".format(code), times])


