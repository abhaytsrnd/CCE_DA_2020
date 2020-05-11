"""App Main

python3 app_main
"""
import os
from dataanalytics.framework.file_utils import FileUtils
FileUtils.mkdir('raw')
FileUtils.mkdir('clean')
from dataanalytics.ux import index

if __name__ == '__main__':
    ""
