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

workbook = xlsxwriter.Workbook('my_report.xlsx')

worksheet = workbook.add_worksheet()

date_format = workbook.add_format({'num_format': 'hh:mm:ss'})
number_format = workbook.add_format()
number_format.set_num_format('0.000')

# Widen the first column to display the dates.
worksheet.set_column('A:A', 10)

log = LogFile("d:\\access_20160925.log")
server_times = log.server_time()
chart_pos = 2

for k in server_times.keys():
    dates = []
    values = []
    logs_count = 0
    # The default chart width x height is 480 x 288 pixels.
    chart = workbook.add_chart({'type': 'line'})
    chart.set_size({'x_scale': 2.5, 'y_scale': 1.2})
    datasheet = workbook.add_worksheet(k)
    for log in server_times[k]:
        logs_count += 1
        date_from_log = time.strptime(log[0], "%d/%b/%Y:%H:%M:%S +0800")
        dates.append(dtime(date_from_log.tm_hour, date_from_log.tm_min, date_from_log.tm_sec))
        values.append(float(log[1]))

    # Write the date to the worksheet.
    datasheet.write_column('A1', dates, date_format)
    datasheet.write_column('B1', values, number_format)

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
    worksheet.insert_chart('D{}'.format(chart_pos), chart)
    chart_pos += 20
workbook.close()
