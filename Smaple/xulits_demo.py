import os
import xlrd
from xlutils.copy import copy
# import xlutils


current=os.path.dirname(__file__)
excel_path=os.path.join(current,'../data/test_case.xls')
workbook=xlrd.open_workbook(excel_path,formatting_info=True)
sheet1=workbook.sheet_by_index(0)

print(sheet1.cell_value(2,14))
#新建一个copy对象，让工作表可以进行写操作
new_workbook = copy(workbook)
sheet = new_workbook.get_sheet(workbook.sheet_names().index('Sheet1'))  #==new_workbook.get_sheet(0)
# sheet.write(2,14,"通过")
# new_workbook.save(excel_path)