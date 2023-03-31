"""
@Time    : 2023/4/1
@Author  : ssw
@File    : export_excel.py
@Desc    :
"""
import os

import xlwt
from io import BytesIO


class ExportExcel:
    """导出excel文件"""

    def __init__(self, excel_name, sheet_name="sheet1", initial_row=0):
        # 创建一个文件对象
        self.wb = xlwt.Workbook(encoding='utf8')
        # 创建一个sheet对象
        self.sheet = self.wb.add_sheet('{}'.format(sheet_name))
        self.style_heading = xlwt.easyxf()
        self.initial_row = initial_row
        self.excel_name = excel_name

    def set_style_heading(self, strg_to_parse):
        self.style_heading = xlwt.easyxf(strg_to_parse)

    def write_heading(self, items):
        for index, i in enumerate(items):
            self.sheet.write(self.initial_row, index, i, self.style_heading)

    def write_data(self, items, keys, data_row=None):
        data_row = self.initial_row + 1 if not data_row else data_row
        for i_dict in items:
            for index, i in enumerate(keys):
                self.sheet.write(data_row, index, i_dict[i])
            data_row += 1

    def save_excel(self, path="static/excel/"):
        exist_file = os.path.exists('{path}{excel_name}.xls'.format(excel_name=self.excel_name, path=path))
        if exist_file:
            os.remove(r'{path}{excel_name}.xls'.format(excel_name=self.excel_name, path=path))
        self.wb.save('{path}{excel_name}.xls'.format(excel_name=self.excel_name, path=path))

    def export(self):
        output = BytesIO()
        self.wb.save(output)
        # 重新定位到开始
        output.seek(0)
        # from django.http import HttpResponse
        # response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
        # response['Content-Disposition'] = 'attachment; filename={}.xls'.format(self.excel_name)
        # response.write(output.getvalue())
        # return response
