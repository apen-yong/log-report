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

workbook = xlsxwriter.Workbook('chart_date_axis.xlsx')

worksheet = workbook.add_worksheet()
chart = workbook.add_chart({'type': 'line'})
date_format = workbook.add_format({'num_format': 'hh:mm:ss'})

# Widen the first column to display the dates.
worksheet.set_column('A:A', 30)

log = LogFile("/Users/yongzhou/access_20160925.log")
server_times = log.server_time()

for k in server_times.keys():
    dates = []
    values = []
    logs_count = 0
    for log in server_times[k]:
        logs_count += 1
        date_from_log = time.strptime(log[0], "%d/%b/%Y:%H:%M:%S +0800")
        dates.append(dtime(date_from_log.tm_hour, date_from_log.tm_min, date_from_log.tm_sec))
        values.append(log[1])

    # Write the date to the worksheet.
    worksheet.write_column('A1', dates, date_format)
    worksheet.write_column('B1', values)

    # Add a series to the chart.
    chart.add_series({
        'categories': '=Sheet1!$A$1:$A${}'.format(logs_count),
        'values': '=Sheet1!$B$1:$B${}'.format(logs_count),
    })

    # Configure the X axis as a Date axis and set the max and min limits.
    chart.set_title({
        'name': u'一天内访问{}的源站的响应时间分布'.format(k),
        'name_font': {
            'color': 'blue',
            'size': 11,
        },
    })

    chart.set_x_axis({
        'name': u'访问时间',
        'date_axis': True,
        'min': dtime(0, 0, 0),
        'max': dtime(23, 59, 59),
    })

    chart.set_y_axis({
        'name': u'响应时间',
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
    worksheet.insert_chart('D2', chart)
    workbook.close()
    exit()
