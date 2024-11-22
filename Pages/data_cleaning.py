from linecache import clearcache

import pandas as pd

data = pd.read_csv("../Data/DataAnalyst.csv", index_col=0)

#Company Name
""" contains one missing value, giving that the description says work at home, we can fill that in
    with "no company" 
"""
cleaned_df = data.copy()
print("copy dataframe:",cleaned_df)
print("Columns:",cleaned_df.columns.tolist())
print("Missing Values:",cleaned_df.isnull().sum())
cleaned_df['Company Name'] = cleaned_df['Company Name'].fillna('Unknown')  # Replace empty strings
cleaned_df['Company Name'] = cleaned_df['Company Name'].replace('1','Unknown')  # Replace -1 to False
print("After Clean Up Total Missing Values:",cleaned_df.isnull().sum())

#East Apply
""" is classified as categorical, but has the values true and -1, therefore, change  -1 to false
"""
print("Unique Values:", cleaned_df['Easy Apply'].unique())
cleaned_df['Easy Apply'] = cleaned_df['Easy Apply'].replace('-1','False')  # Replace -1 to False
print("Unique Values:", cleaned_df['Easy Apply'].unique())

#alot of -1 occurrences replace it with unknown
# Moderate to Large Missing Percentage:
# Replace missing values with a placeholder like "Unknown", "Other", or "Missing"
cleaned_df['Salary Estimate'] = cleaned_df['Salary Estimate'].replace('-1','Unknown')  # Replace -1 to False
#given large number of occurrences of -1 --> 7.63%
# Count how many values in the 'Location' column occurred as a percentage of occurrences
value_counts = cleaned_df['Headquarters'].value_counts(normalize=True) * 100
# Print the result
for value, percentage in value_counts.items():
    print(f"{value} --> {percentage:.2f}%")
cleaned_df['Headquarters'] = cleaned_df['Headquarters'].replace('-1','Unknown')
print("Unique Values:", cleaned_df['Headquarters'].unique())

# Small Missing Percentage (<5%):
# Replace missing values with the most frequent category (mode)
#since Size --> has -1 for 3 observations, we use most frequent category, which is 51 to 200 employees
print("Unique Values:", cleaned_df['Size'].unique())
cleaned_df['Size'] = cleaned_df['Size'].replace('-1','51 to 200 employees')
print("Unique Values:", cleaned_df['Size'].unique())