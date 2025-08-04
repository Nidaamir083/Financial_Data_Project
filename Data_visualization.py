#Generate a bar chart to visualize the total amount by document type using the aggregated data.
import matplotlib.pyplot as plt

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(document_type_summary.index, document_type_summary['Total Amount (LCY)'])

# Add title and labels
plt.title('Total Amount (LCY) by Document Type')
plt.xlabel('Document Type')
plt.ylabel('Total Amount (LCY)')

# Rotate x-axis labels for better readability if needed
plt.xticks(rotation=45, ha='right')

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# Display the plot
plt.show()

##The document_type_summary dataframe, containing aggregated data of 'Total Amount (LCY)' by 'Document Type', was selected for visualization.
##A bar chart was chosen as the visualization type to compare the total amounts across different document types.
##A bar chart was successfully generated and displayed, illustrating the total amount for each document type.


# Plot a histogram of the 'Amount (LCY)' column for 'Invoice' entries
plt.figure(figsize=(10, 6))
plt.hist(highest_amount_df['Amount (LCY)'].dropna(), bins=50, edgecolor='black')

# Add title and labels
plt.title('Distribution of Amount (LCY) for Invoice Document Type')
plt.xlabel('Amount (LCY)')
plt.ylabel('Frequency')

# Use scientific notation for the y-axis if needed
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()

##The document_type_summary dataframe, containing aggregated data of 'Total Amount (LCY)' by 'Document Type', was selected for visualization.
##A bar chart was chosen as the visualization type to compare the total amounts across different document types.
##A bar chart was successfully generated and displayed, illustrating the total amount for each document type
