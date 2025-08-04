# Financial_Data_Project
Build a robust financial data parsing system that can process Excel files, intelligently detect data types, handle various formats, and store data in optimized structures for fast retrieval.

##Step 1:
Load Excel sheets and inspect Data like number of rows and columns by info function
Preview excel sheet 

##Detect Column type:
Whether the column is Object, String or Float

##Step 2:
Implement intelligent column classification
Detection Strategy:
def detect_column_type(column_data):
# Remove null values for analysis
# Try parsing as dates first
# Try parsing as numbers (handle currency symbols)
# Default to string if neither works
# Return confidence score for each type

##Step 3: Format Parsing Challenges:
Amount Formats to Handle
Date Formats to Handle

##Step 4: Data Structure Implementation:
 Fast lookup by multiple criteria
 Memory efficient storage
 Support for range queries (date ranges, amount ranges)
 Easy aggregation capabilities


