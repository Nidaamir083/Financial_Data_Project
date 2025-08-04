#Explore potential ways to join or merge the 'KH_Bank_Cleaned' and 'Customer_Ledger_Entries_Cleaned' datasets based on common columns.

##Print the columns of both dataframes to identify potential join keys.
print("Columns in KH_Bank_Cleaned:")
print(df_cleaned.columns.tolist())

print("\nColumns in Customer_Ledger_Entries_Cleaned:")
print(df_cleaned_2.columns.tolist())


# Define the columns for merging
bank_date_col = 'Statement.Entry.BookingDate.Date'
bank_amount_col = 'Statement.Entry.Amount.Value'
ledger_date_col = 'Posting Date'
ledger_amount_col = 'Amount (LCY)'

# Perform an inner merge
merged_df = pd.merge(
    df_cleaned,
    df_cleaned_2,
    left_on=[bank_date_col, bank_amount_col],
    right_on=[ledger_date_col, ledger_amount_col],
    how='inner'
)

# Print the shape of the merged dataframe
print("Shape of the merged dataframe:", merged_df.shape)

# Display the first few rows of the merged dataframe
print("\nMerged Dataframe (first 5 rows):")
display(merged_df.head())



#Data Analysis Key Findings
##The datasets KH_Bank_Cleaned and Customer_Ledger_Entries_Cleaned were analyzed to find potential common columns for merging. The columns 'Statement.Entry.BookingDate.Date' and 'Statement.Entry.Amount.Value' from the first dataset, and 'Posting Date' and 'Amount (LCY)' from the second, were identified as potential join keys.
##An inner merge was performed on the two datasets using the identified date and amount columns as keys.
##The resulting merged dataframe was empty, with a shape of (0, 100). This indicates that there were no exact matches between the two datasets based on the selected date and amount columns.
#Insights or Next Steps
##The lack of matching records suggests that a direct merge on date and amount is not viable. Further investigation is needed to explore fuzzy matching techniques or to identify more reliable common identifiers for joining the datasets.
