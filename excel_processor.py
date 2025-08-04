# Create the src/ directory and write the ExcelProcessor class to excel_processor.py and an empty __init__.py
src_dir = Path("/mnt/data/src")
src_dir.mkdir(parents=True, exist_ok=True)

# Write excel_processor.py
excel_processor_code = '''\
import pandas as pd
import openpyxl
import numpy as np
import re
from datetime import datetime
from dateutil.parser import parse


class ExcelProcessor:
    def __init__(self):
        self.workbooks = {}

    def load_files(self, file_paths):
        for path in file_paths:
            try:
                self.workbooks[path] = pd.read_excel(path, sheet_name=None, engine='openpyxl')
                print(f"Loaded: {path} ✅")
            except Exception as e:
                print(f"Error loading {path}: {e}")

    def get_sheet_info(self):
        for file, sheets in self.workbooks.items():
            print(f"\\n📁 File: {file}")
            for sheet_name, df in sheets.items():
                print(f"  🧾 Sheet: {sheet_name}")
                print(f"    ➤ Shape: {df.shape[0]} rows × {df.shape[1]} columns")
                print(f"    ➤ Columns: {list(df.columns)}\\n")

    def extract_data(self, file, sheet_name):
        return self.workbooks[file][sheet_name]

    def preview_data(self, file, sheet_name, rows=5):
        df = self.extract_data(file, sheet_name)
        print(df.head(rows))
'''

excel_processor_path = src_dir / "excel_processor.py"
excel_processor_path.write_text(excel_processor_code)

# Create __init__.py
(src_dir / "__init__.py").write_text("")

# Return download links
excel_processor_path.name, str(excel_processor_path), "/mnt/data/src/__init__.py"
