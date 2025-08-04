import re
from datetime import datetime, timedelta

class FormatParser:
    def parse_amount(self, value, detected_format=None):
        if pd.isna(value):
            return None
        if isinstance(value, (int, float)):
            return float(value)

        original = str(value).strip()
        cleaned = original.replace('₹', '').replace('$', '').replace('€', '')
        cleaned = cleaned.replace(',', '').replace('(', '-').replace(')', '')
        cleaned = cleaned.replace('–', '-')  # Handle en-dash

        # Handle trailing negative (e.g., 1234.56-)
        if re.match(r'.*-\s*$', cleaned):
            cleaned = '-' + cleaned.replace('-', '')

        # Handle abbreviated formats
        if re.match(r'^\d+(\.\d+)?[KMB]$', cleaned, re.IGNORECASE):
            factor = {'K': 1e3, 'M': 1e6, 'B': 1e9}
            unit = cleaned[-1].upper()
            return float(cleaned[:-1]) * factor[unit]

        try:
            return float(cleaned)
        except:
            return None

    def parse_date(self, value, detected_format=None):
        if pd.isna(value):
            return None

        if isinstance(value, (int, float)) and value > 30000:
            # Excel serial date (starts at 1899-12-30)
            base_date = datetime(1899, 12, 30)
            return (base_date + timedelta(days=int(value))).date()

        value = str(value).strip()

        # Quarter formats
        if match := re.match(r'[Qq](\d)[\s\-]?(\d{2,4})', value):
            q, year = match.groups()
            year = int(year) if len(year) == 4 else 2000 + int(year)
            month = (int(q) - 1) * 3 + 1
            return datetime(year, month, 1).date()

        # Month-Year formats (e.g., Mar 2024)
        month_map = {
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
            'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
            'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        if match := re.match(r'([A-Za-z]+)[\s\-]?(\d{2,4})', value):
            month_str, year = match.groups()
            month_str = month_str[:3].lower()
            if month_str in month_map:
                year = int(year) if len(year) == 4 else 2000 + int(year)
                return datetime(year, month_map[month_str], 1).date()

        # Try common date formats
        formats = ["%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d", "%d-%b-%Y", "%b-%y", "%B %Y"]
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt).date()
            except:
                continue

        # Fallback to fuzzy parsing
        try:
            return pd.to_datetime(value, errors='coerce').date()
        except:
            return None

    def normalize_currency(self, value):
        if isinstance(value, str):
            return re.sub(r'[^\d\.\-]', '', value)
        return value

    def handle_special_formats(self, value):
        """
        Catch and handle anything unexpected
        """
        if isinstance(value, str):
            value = value.strip()
            if value.lower() in ['na', 'n/a', '-', '']:
                return None
        return value

parser = FormatParser()

amounts = [
    "$1,234.56", "(2,500.00)", "€1.234,56", "1.5M", "₹1,23,456", "1234.56-", "123456"
]

for a in amounts:
    print(f"{a} → {parser.parse_amount(a)}")

dates = [
    "12/31/2023", "2023-12-31", "Q4 2023", "Mar-24", "March 2024", "44927"
]

for d in dates:
    print(f"{d} → {parser.parse_date(d)}")


import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta

# Redundant FinancialDataStore class removed to avoid confusion.
# The DataStorage class in cell ch_RqtUj7MD3 will be used instead.

def normalize_dataframe(df, detector, parser):
    """
    Normalizes a single dataframe based on detected column types.

    Args:
        df (pd.DataFrame): The input dataframe to normalize.
        detector (DataTypeDetector): An instance of DataTypeDetector.
        parser (FormatParser): An instance of FormatParser.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: The normalized dataframe.
            - dict: A dictionary of column types for the dataframe.
    """
    column_types = {}
    df_cleaned = df.copy()

    for col in df.columns:
        result = detector.analyze_column(col, df[col])
        dtype = result['type']
        column_types[col] = dtype

        if dtype == 'NUMBER':
            df_cleaned[col] = df[col].apply(lambda x: parser.parse_amount(x))
        elif dtype == 'DATE':
            df_cleaned[col] = df[col].apply(lambda x: parser.parse_date(x))
        else:
            df_cleaned[col] = df[col]  # keep string as-is

    return df_cleaned, column_types


import pandas as pd
import numpy as np

class DataStorage:
    def __init__(self):
        self.data = {}
        self.metadata = {}
        self.indexes = {}

    def store_data(self, name, dataframe, metadata):
        """Stores a dataframe and its metadata."""
        self.data[name] = dataframe
        self.metadata[name] = metadata
        self.indexes[name] = {}
        print(f"Dataframe '{name}' stored.")

    def create_indexes(self, dataset_name, columns):
        """Creates indexes for specified columns in a dataset."""
        if dataset_name not in self.data:
            print(f"Dataset '{dataset_name}' not found.")
            return

        df = self.data[dataset_name]
        for col in columns:
            if col in df.columns:
                # For demonstration, creating a simple index (e.g., sorted unique values)
                # More advanced indexing (e.g., B-trees, hash maps) would be needed for large datasets
                self.indexes[dataset_name][col] = sorted(df[col].dropna().unique())
                print(f"Index created for column '{col}' in dataset '{dataset_name}'.")
            else:
                print(f"Column '{col}' not found in dataset '{dataset_name}'.")


    def query_by_criteria(self, dataset_name, filters):
        """
        Queries the dataset based on multiple criteria with support for range queries.

        filters is a dictionary where keys are column names and values are:
        - a single value for exact match
        - a tuple (min, max) for range queries (inclusive)
        - a list of values for multiple exact matches
        """
        if dataset_name not in self.data:
            print(f"Dataset '{dataset_name}' not found.")
            return pd.DataFrame()

        df = self.data[dataset_name]
        filtered_df = df.copy()

        for col, criteria in filters.items():
            if col not in filtered_df.columns:
                print(f"Warning: Column '{col}' not found in dataset '{dataset_name}'. Skipping filter.")
                continue

            if isinstance(criteria, tuple) and len(criteria) == 2:
                # Range query
                min_val, max_val = criteria
                filtered_df = filtered_df[
                    (filtered_df[col] >= min_val) & (filtered_df[col] <= max_val)
                ]
            elif isinstance(criteria, list):
                 # Multiple exact matches
                 filtered_df = filtered_df[filtered_df[col].isin(criteria)]
            else:
                # Exact match
                filtered_df = filtered_df[filtered_df[col] == criteria]

        return filtered_df

    def aggregate_data(self, dataset_name, group_by=None, measures=None):
        """
        Aggregates data based on grouping criteria and calculates specified measures.

        group_by: list of column names to group by.
        measures: dictionary where keys are new column names and values are tuples
                  (original_column, aggregation_function, *args for function).
                  Aggregation function can be a string ('sum', 'mean', 'count', etc.)
                  or a callable function.
        """
        if dataset_name not in self.data:
            print(f"Dataset '{dataset_name}' not found.")
            return pd.DataFrame()

        df = self.data[dataset_name]

        if not group_by and not measures:
            return df # Return original if no aggregation specified

        if group_by:
            # Check if group_by columns exist
            if not all(col in df.columns for col in group_by):
                print("Error: One or more group_by columns not found.")
                return pd.DataFrame()

        if measures:
            agg_dict = {}
            for new_col, (original_col, func, *args) in measures.items():
                if original_col not in df.columns:
                    print(f"Warning: Original column '{original_col}' for measure '{new_col}' not found. Skipping.")
                    continue

                if isinstance(func, str):
                    agg_dict[new_col] = pd.NamedAgg(column=original_col, aggfunc=func)
                elif callable(func):
                     agg_dict[new_col] = pd.NamedAgg(column=original_col, aggfunc=lambda x: func(x, *args))
                else:
                    print(f"Warning: Unknown aggregation function type for measure '{new_col}'. Skipping.")
                    continue

            if group_by:
                return df.groupby(group_by).agg(**agg_dict)
            else:
                # Aggregate without grouping
                return df.agg(**agg_dict)

        return df # Return original if no measures specified but group_by is empty

# Initialize components
detector = DataTypeDetector()
parser = FormatParser()
store = DataStorage()

# Choose sheet from your Excel file
file_path = '/content/KH_Bank.XLSX'
sheet_name = list(processor.workbooks[file_path].keys())[0]  # First sheet
df = processor.extract_data(file_path, sheet_name)

file_path_2 = '/content/Customer_Ledger_Entries_FULL.xlsx'
sheet_name_2 = list(processor.workbooks[file_path_2].keys())[0]  # First sheet
df_2 = processor.extract_data(file_path_2, sheet_name_2)

# Normalize and classify
df_cleaned, column_types = normalize_dataframe(df, detector, parser)
df_cleaned_2, column_types_2 = normalize_dataframe(df_2, detector, parser)


# Store cleaned data
store.store_data(name='KH_Bank_Cleaned', dataframe=df_cleaned, metadata=column_types)
store.store_data(name='Customer_Ledger_Entries_Cleaned', dataframe=df_cleaned_2, metadata=column_types_2)

# View the cleaned output
df_cleaned.head()
df_cleaned_2.head()

# Choose sheet from the second Excel file
file_path_2 = '/content/Customer_Ledger_Entries_FULL.xlsx'
sheet_name_2 = list(processor.workbooks[file_path_2].keys())[0]  # First sheet of the second file
df_2 = processor.extract_data(file_path_2, sheet_name_2)

# Normalize and classify the second dataframe
df_cleaned_2, column_types_2 = normalize_dataframe(df_2, detector, parser)

# Store cleaned data for the second file
store.store_data(name='Customer_Ledger_Entries_Cleaned', dataframe=df_cleaned_2, metadata=column_types_2)

# View the cleaned output for the second file
print("\nCleaned Data from Customer_Ledger_Entries_FULL.xlsx:")
display(df_cleaned_2.head())
