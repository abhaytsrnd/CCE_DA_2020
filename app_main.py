"""App Main

python3 app_main
"""
import os
from dataanalytics.framework.file_utils import FileUtils
FileUtils.mkdir('raw')
FileUtils.mkdir('clean')

from dataanalytics.framework.database import db
clean_files = FileUtils.files('clean')
tags = {'empty': 1}
db.put('tags', tags)
for file in clean_files:
    tags[file] = 1

from dataanalytics.ux import index

if __name__ == '__main__':
    ""
