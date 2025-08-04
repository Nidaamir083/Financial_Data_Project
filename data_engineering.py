# Example of a more complex query with multiple filters

complex_filters = {
    'Document Type': 'Invoice',
    'Customer No.': 'CTTP000005',  # Replace with an actual Customer No. from your data
    'Posting Date': (datetime(2023, 1, 1).date(), datetime(2023, 12, 31).date()) # Example date range
}

complex_query_results = store.query_by_criteria(
    dataset_name='Customer_Ledger_Entries_Cleaned',
    filters=complex_filters
)

print("\nComplex Query Results (first 5 rows):")
display(complex_query_results.head())
print(f"\nTotal number of entries matching the complex criteria: {len(complex_query_results)}")

#Determine the document type with the highest total amount from the aggregated summary.
highest_amount_doc_type = document_type_summary['Total Amount (LCY)'].idxmax()

print(f"The document type with the highest total amount (LCY) is: {highest_amount_doc_type}")

#Filter the original Customer_Ledger_Entries_Cleaned dataframe to include only the entries corresponding to the identified highest amount document type.
highest_amount_doc_type = document_type_summary['Total Amount (LCY)'].idxmax()

highest_amount_df = store.query_by_criteria(
    dataset_name='Customer_Ledger_Entries_Cleaned',
    filters={'Document Type': highest_amount_doc_type}
)

print(f"\nFiltered data for document type: {highest_amount_doc_type}")
display(highest_amount_df.head())

#Calculate descriptive statistics for numerical columns in the filtered dataframe and display them
# Identify numerical columns in the filtered dataframe
numerical_cols = highest_amount_df.select_dtypes(include=np.number).columns

# Calculate descriptive statistics for numerical columns
descriptive_stats = highest_amount_df[numerical_cols].describe()

# Display the descriptive statistics
print("\nDescriptive Statistics for Numerical Columns in 'Invoice' Entries:")
display(descriptive_stats)

#Filter the 'Invoice' dataframe to show entries with large positive and negative 'Amount (LCY)' values to investigate potential anomalies.
# Define thresholds for large positive and negative amounts (adjust as needed)
positive_threshold = highest_amount_df['Amount (LCY)'].quantile(0.95) # Top 5%
negative_threshold = highest_amount_df['Amount (LCY)'].quantile(0.05) # Bottom 5%

print(f"\nInvestigating large positive amounts (above {positive_threshold:.2f}):")
large_positive_amounts = highest_amount_df[highest_amount_df['Amount (LCY)'] > positive_threshold]
display(large_positive_amounts.sort_values(by='Amount (LCY)', ascending=False).head()) # Display top 5 largest

print(f"\nInvestigating large negative amounts (below {negative_threshold:.2f}):")
large_negative_amounts = highest_amount_df[highest_amount_df['Amount (LCY)'] < negative_threshold]
display(large_negative_amounts.sort_values(by='Amount (LCY)', ascending=True).head()) # Display top 5 smallest (most negative)

#Group the filtered 'Invoice' dataframe by 'Customer Name' and calculate the sum of 'Amount (LCY)' for each customer.
# Group 'Invoice' data by 'Customer Name' and calculate the sum of 'Amount (LCY)'
customer_invoice_summary = highest_amount_df.groupby('Customer Name')['Amount (LCY)'].sum().sort_values(ascending=False)

print("\nTotal Invoice Amount (LCY) by Customer:")
display(customer_invoice_summary.head()) # Display top 5 customers by total amount
print(f"\nTotal number of customers with invoice entries: {len(customer_invoice_summary)}")
