"""
requirements:
    pip install xlrd
    pip install xlwt
    pip install openpyxl
    pip install pandas
"""

import pandas as pd


def save2xls(file_name, data_dict):
    writer = pd.ExcelWriter(file_name)
    df1 = pd.DataFrame(data_dict)
    df1.to_excel(writer, sheet_name='mac vs masterkey', header=False, index=False)
    writer.save()


if __name__ == "__main__":

    data_test = {"h1": ['h1_1','h1_2','h1_3'], "h2": ['h2_1','h2_2','h2_3']}
    save2xls('test.xlsx', data_test)
