import pandas as pd
import openpyxl
import numpy as np
import re
from dateutil.parser import parse
from datetime import datetime

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
            print(f"\n📁 File: {file}")
            for sheet_name, df in sheets.items():
                print(f"  🧾 Sheet: {sheet_name}")
                print(f"    ➤ Shape: {df.shape[0]} rows × {df.shape[1]} columns")
                print(f"    ➤ Columns: {list(df.columns)}\n")

    def extract_data(self, file, sheet_name):
        return self.workbooks[file][sheet_name]

    def preview_data(self, file, sheet_name, rows=5):
        df = self.extract_data(file, sheet_name)
        print(df.head(rows))


class DataTypeDetector:
    def detect_column_type(self, column_data):
        non_null_data = column_data.dropna()

        date_count = 0
        number_count = 0

        for val in non_null_data[:20]:  # Sample first 20 non-null values
            if self.is_date(val):
                date_count += 1
            elif self.is_number(val):
                number_count += 1

        total = len(non_null_data[:20])
        if total > 0: # Avoid division by zero
            if date_count / total > 0.6:
                return "DATE"
            elif number_count / total > 0.6:
                return "NUMBER"
            else:
                return "STRING"
        else:
            return "STRING" # Default to string if no non-null data

    def is_date(self, value):
        try:
            parse(str(value), fuzzy=False)
            return True
        except:
            return False

    def is_number(self, value):
        try:
            val = str(value).replace(",", "").replace("$", "").replace("(", "-").replace(")", "")
            float(val)
            return True
        except:
            return False

# === Usage Example ===

# Instantiate and load Excel files
processor = ExcelProcessor()
file_paths = [
    '/content/KH_Bank.XLSX',
    '/content/Customer_Ledger_Entries_FULL.xlsx'
]
processor.load_files(file_paths)

# View file & sheet info
processor.get_sheet_info()

# Detect data types in a specific sheet
detector = DataTypeDetector()
# Use the full file path as the key
sample_df = processor.extract_data('/content/KH_Bank.XLSX', list(processor.workbooks['/content/KH_Bank.XLSX'].keys())[0])  # First sheet

print("\n📊 Column Type Detection:")
for col in sample_df.columns:
    dtype = detector.detect_column_type(sample_df[col])
    print(f"{col}: {dtype}")



detector = DataTypeDetector()
df = processor.extract_data('/content/KH_Bank.XLSX', 'Sheet1')  # Replace with actual sheet name

print("\n📊 Column Classification:")
for col in df.columns:
    result = detector.analyze_column(col, df[col])
    print(f"🧾 {col}:")
    print(f"  ➤ Type: {result['type']}")
    print(f"  ➤ Confidence: {result['confidence']}")
    print(f"  ➤ Format Info: {result['format']}\n")

detector = DataTypeDetector()
df1 = processor.extract_data('/content/Customer_Ledger_Entries_FULL.xlsx', 'Customer Ledger Entries')  # Replace with actual sheet name

print("\n📊 Column Classification:")
for col in df1.columns:
    result = detector.analyze_column(col, df1[col])
    print(f"🧾 {col}:")
    print(f"  ➤ Type: {result['type']}")
    print(f"  ➤ Confidence: {result['confidence']}")
    print(f"  ➤ Format Info: {result['format']}\n")


detector = DataTypeDetector()
df1 = processor.extract_data('/content/Customer_Ledger_Entries_FULL.xlsx', 'Customer Ledger Entries')  # Replace with actual sheet name

print("\n📊 Column Classification:")
for col in df1.columns:
    result = detector.analyze_column(col, df1[col])
    print(f"🧾 {col}:")
    print(f"  ➤ Type: {result['type']}")
    print(f"  ➤ Confidence: {result['confidence']}")
    print(f"  ➤ Format Info: {result['format']}\n")
