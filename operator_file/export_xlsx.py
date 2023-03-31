"""
@Time    : 2023/4/1
@Author  : ssw
@File    : export_excel.py
@Desc    :
"""
import os
from datetime import datetime

import xlsxwriter
from io import BytesIO


class ExportXlsx(object):
    """导出xlsx文件"""

    def __init__(self):
        self.output = BytesIO()
        self.workbook = xlsxwriter.Workbook(self.output)
        self.worksheet = self.workbook.add_worksheet()
        self.bold = self.workbook.add_format({'bold': 1})

    def set_column_width(self, column_width_dict):
        """设置列宽"""
        for key, value in column_width_dict.items():
            self.worksheet.set_column(key, key, value)

    def set_header(self, header_list):
        col = 0
        for i in header_list:
            self.worksheet.write(0, col, i, self.bold)
            col += 1

    def write_data(self, instance_list, keys, foreign_keys):
        row = 1
        print(len(instance_list), instance_list)
        for instance in instance_list:
            foreign_key_index = 0
            for index, i in enumerate(keys):
                value = getattr(instance, i)
                if isinstance(value, int):
                    self.worksheet.write_number(row, index, value)
                elif isinstance(value, datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                    self.worksheet.write_string(row, index, value)
                elif isinstance(value, str):
                    self.worksheet.write_string(row, index, value)
                else:
                    if value:
                        foreign_key = getattr(value, foreign_keys[foreign_key_index]) if foreign_keys else value.id
                        self.worksheet.write_string(row, index, str(foreign_key))
                        foreign_key_index += 1
            row += 1
        self.workbook.close()

    def export(self, header_list, instance_list, keys, file_name, foreign_keys=None):
        self.set_header(header_list)
        self.write_data(instance_list, keys, foreign_keys)
        self.output.seek(0)
        # response = HttpResponse(self.output.read(),
        #                         content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        # response['Content-Disposition'] = "attachment; filename={}.xlsx".format(file_name)
        # return response
