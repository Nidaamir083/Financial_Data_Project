invoice_entries = store.query_by_criteria(
    dataset_name='Customer_Ledger_Entries_Cleaned',
    filters={'Document Type': 'Invoice'}
)

print("\nInvoice Entries:")
display(invoice_entries.head())
print(f"\nTotal number of invoice entries: {len(invoice_entries)}")

amount_filtered_entries = store.query_by_criteria(
    dataset_name='KH_Bank_Cleaned',
    filters={'Statement.Entry.Amount.Value': (1000.0, 5000.0)}
)

print("\nBank Entries with Amount between 1000 and 5000:")
display(amount_filtered_entries.head())
print(f"\nTotal number of entries in the specified amount range: {len(amount_filtered_entries)}")


document_type_summary = store.aggregate_data(
    dataset_name='Customer_Ledger_Entries_Cleaned',
    group_by=['Document Type'],
    measures={'Total Amount (LCY)': ('Amount (LCY)', 'sum')}
)

print("\nTotal Amount (LCY) by Document Type:")
display(document_type_summary)
