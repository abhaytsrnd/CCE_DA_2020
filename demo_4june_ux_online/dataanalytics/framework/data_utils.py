from dataanalytics.framework.file_utils import FileUtils
import pandas as pd

N = 5

class DataUtils:

    @staticmethod
    def read_text_head(path: str):
        format = FileUtils.file_format(path)
        op = None
        if format == 'csv' or format == 'txt':
            with open(path) as myfile:
                head = [next(myfile).strip() for x in range(N)]
            op = head
        return op

    @staticmethod
    def read_csv(path: str, sep: str, header: bool):
        if header:
            df = pd.read_csv(path, sep = sep)
        else:
            df = pd.read_csv(path, sep = sep, header = None)
            df = df.add_prefix('col')
        return df

    @staticmethod
    def read_xls(path: str, sheet: str, header: bool):
        xls = pd.ExcelFile(path)
        if header:
            df = pd.read_excel(xls, sheet)
        else:
            df = pd.read_excel(xls, sheet, header = None)
            df = df.add_prefix('col')
        return df

    @staticmethod
    def read(dir:str, filename: str):
        format = FileUtils.file_format(filename)
        path = FileUtils.path(dir, filename)
        op = None
        if format == 'csv' or format == 'txt':
            with open(path) as myfile:
                head = [next(myfile).strip() for x in range(N)]
            op = head
        elif format == 'jpeg' or format == 'jpg' or format == 'gif':
            ""
        else:
            op = "Format Not Supported!!"
        return op
