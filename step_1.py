# Step 1: Create instance
processor = ExcelProcessor()

# Step 2: Load files
processor.load_files([
    '/content/KH_Bank.XLSX',
    '/content/Customer_Ledger_Entries_FULL.xlsx'
])

# Step 3: Show sheet info
processor.get_sheet_info()

# Step 4: Optional - preview a sheet
processor.preview_data('/content/KH_Bank.XLSX', 'Sheet1')  # Corrected file path

processor.preview_data('/content/Customer_Ledger_Entries_FULL.xlsx', 'Customer Ledger Entries')  # Corrected file path
