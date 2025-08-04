import pandas as pd

def read_excel_file(filepath):
    df = pd.read_excel(filepath)
    return df

def summarize_dataframe(df):
    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "nulls": df.isnull().sum().to_dict()
    }
