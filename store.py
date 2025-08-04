store.store_data(name='KH_Bank_Cleaned', dataframe=df_cleaned, metadata=column_types)
store.store_data(name='Customer_Ledger_Entries_Cleaned', dataframe=df_cleaned_2, metadata=column_types_2)

print("\nDatasets currently in storage:")
print(list(store.data.keys()))
