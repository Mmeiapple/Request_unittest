import os
import xlrd


class Excel_utils():
    def __init__(self,data_path,sheet_name):
        self.data_path=data_path
        self.sheet_name=sheet_name
        self.sheet=self.open_sheet()

    '''打开工作表'''

    def open_sheet(self):
        self.workbook=xlrd.open_workbook(self.data_path)
        self.sheet=self.workbook.sheet_by_name(self.sheet_name)
        return self.sheet

    '''获取最大行数'''

    def get_row_count(self):
        nrows=self.sheet.nrows
        return nrows

    '''获取最大列数'''

    def get_col_count(self):
        cols=self.sheet.ncols
        return cols

    '''获取行值'''

    def get_cell_value(self,row_index,col_index):
        call_value=self.sheet.cell_value(row_index,col_index)
        return call_value

    '''获取合并单元格数量'''

    def get_merged_index(self):
        return self.sheet.merged_cellsq



    """既能获取普通单元格的数据又能获取合并单元格数据"""

    def get_merged_cell_value(self,row_index,col_index):
        call_values = None
        # 遍历合并单元格的起始行和结束行、起始列、结束列
        for (rlow, rhigh, clow, chigh) in self.get_merged_index():
            # 判断行数是否在合并单元格的行内
            if (row_index >= rlow and row_index < rhigh):
                # 判断列数是否在合并单元格的列内
                if (col_index >= clow and col_index < chigh):
                    call_values = self.sheet.cell_value(rlow, clow)
                    break;
                else:
                    call_values = self.sheet.cell_value(row_index, col_index)
            else:
                call_values = self.sheet.cell_value(row_index, col_index)

        return call_values



if __name__=="__main__":
    current=os.path.dirname(__file__)
    path_data_file=os.path.join(current,'../data/test_case.xlsx')
    print(path_data_file)
    vaule=Excel_utils(path_data_file,'Sheet1').get_merged_cell_value(0,1)
    print(vaule)


