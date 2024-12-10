import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv("../Data/DataAnalyst.csv", index_col=0)

#Company Name
""" contains one missing value, giving that the description says work at home, we can fill that in
    with "no company" 
"""
cleaned_df = data.copy()
cleaned_df = cleaned_df.reset_index()
print("copy dataframe:",cleaned_df)
print("Columns:",cleaned_df.columns.tolist())
print("Missing Values:",cleaned_df.isnull().sum())

# Function to count -1 occurrences in each column
def count_negative_ones(df):
    for column in df.columns:
        count = (df[column] == '-1').sum()
        print(f"Column: {column}, Total '-1' values: {count}")

# Call the function with the cleaned dataframe
count_negative_ones(cleaned_df)

def print_unique_value_percentages(df, column_name):
    value_counts = df[column_name].value_counts(normalize=True) * 100
    for value, percentage in value_counts.items():
        print(f"{value} --> {percentage:.2f}%")



#Job Title
# Mapping similar job titles to a unified name
job_title_mapping = {
    "Sr. Data Analyst": "Senior Data Analyst",
    "Senior Data Analyst": "Senior Data Analyst",
    "Data Analyst Junior": "Junior Data Analyst",
    "Junior Data Analyst": "Junior Data Analyst"
}
# Replace job titles using the mapping
cleaned_df["Job Title"] = cleaned_df["Job Title"].replace(job_title_mapping)
print(cleaned_df['Job Title'].value_counts()[:20])


#Salary Estimates
# print("Unique Values:", cleaned_df['Salary Estimate'].unique())
#print_unique_value_percentages(cleaned_df, 'Salary Estimate')
#value_counts = cleaned_df['Salary Estimate'].value_counts(normalize=True) * 100
# Print the result
# for value, percentage in value_counts.items():
#     print(f"{value} --> {percentage:.2f}%")

# Small Missing Percentage (<5%):
# Replace missing values with the most frequent category (mode)
#since Size --> has -1 for 1 observation, we use most frequent category, which is $41K-$78K (Glassdoor est.)
cleaned_df['Salary Estimate'] = cleaned_df['Salary Estimate'].replace('-1','$41K-$78K (Glassdoor est.)')
# print("Unique Values:", cleaned_df['Salary Estimate'].unique())
#print_unique_value_percentages(cleaned_df, 'Salary Estimate')


# Company Name
cleaned_df['Company Name'] = cleaned_df['Company Name'].fillna('Unknown')  # Replace empty strings
cleaned_df['Company Name'] = cleaned_df['Company Name'].replace('1','Unknown')  # Replace -1 to False
cleaned_df['Company Name'] = cleaned_df['Company Name'].str.split(r'\r\n').str[0] # move everything from the backslashes
#print("After Clean Up Total Missing Values:",cleaned_df.isnull().sum())

#Headquarters
#print_unique_value_percentages(cleaned_df, 'Headquarters') # output -1 --> 7.63% occurence
#large missing values change to Unknown
cleaned_df['Headquarters'] = cleaned_df['Headquarters'].replace('-1','Unknown')
#print_unique_value_percentages(cleaned_df, 'Headquarters')

#Rating
#print_unique_value_percentages(cleaned_df, 'Rating')
#Use NaN if -1 is invalid or unknown: It maintains numeric integrity and allows for future imputation or exclusion.
cleaned_df['Rating'] = cleaned_df['Rating'].replace(-1, np.nan)
#print_unique_value_percentages(cleaned_df, 'Rating')


#Size
# print_unique_value_percentages(cleaned_df, 'Size')
# Small Missing Percentage (<5%):
# Replace missing values with the most frequent category (mode)
#since Size --> has -1 to (Unknown) we use most frequent category, which is 51 to 200 employees
cleaned_df['Size'] = cleaned_df['Size'].replace('-1','51 to 200 employees')
#print_unique_value_percentages(cleaned_df, 'Size')

#Founded
#print_unique_value_percentages(cleaned_df, 'Founded')
#Use NaN if -1 is invalid or unknown: It maintains numeric integrity and allows for future imputation or exclusion.
cleaned_df['Founded'] = cleaned_df['Founded'].replace(-1, np.nan)
#print_unique_value_percentages(cleaned_df, 'Founded')


#Type of Ownership
#print_unique_value_percentages(cleaned_df, 'Type of ownership')
cleaned_df['Type of ownership'] = cleaned_df['Type of ownership'].replace('-1','Unknown')
#print_unique_value_percentages(cleaned_df, 'Type of ownership')


#Type of Industry
# print_unique_value_percentages(cleaned_df, 'Industry')
cleaned_df['Industry'] = cleaned_df['Industry'].replace('-1','Unknown')
# print_unique_value_percentages(cleaned_df, 'Industry')


#Sector
# print_unique_value_percentages(cleaned_df, 'Sector')
cleaned_df['Sector'] = cleaned_df['Sector'].replace('-1','Unknown')
# print_unique_value_percentages(cleaned_df, 'Sector')


#Revenue
# print_unique_value_percentages(cleaned_df, 'Revenue')
cleaned_df['Revenue'] = cleaned_df['Revenue'].replace("-1", np.nan)
#print_unique_value_percentages(cleaned_df, 'Revenue')

#Competitors
# print_unique_value_percentages(cleaned_df, 'Competitors')
cleaned_df['Competitors'] = cleaned_df['Competitors'].replace('-1','Unknown')
# print_unique_value_percentages(cleaned_df, 'Competitors')


#Easy Apply
""" is classified as categorical, but has the values true and -1, therefore, change  -1 to false
"""
# print("Unique Values:", cleaned_df['Easy Apply'].unique())
cleaned_df['Easy Apply'] = cleaned_df['Easy Apply'].replace('-1','False')  # Replace -1 to False
cleaned_df['Easy Apply'] = cleaned_df['Easy Apply'].fillna(False).astype('bool')
# print(type(cleaned_df['Easy Apply'][0]))
# print("Unique Values:", cleaned_df['Easy Apply'].unique())


#Split Salary Estimate into Min & Max columns
""" 
Separate into numeric columns make it easier to perform analysis, like finding averages or ranges.
You can compare minimum and maximum salaries across different jobs or filter data by specific salary ranges.
It removes the non-essential text (e.g., "Glassdoor est.") from the salary information.
"""
# Improved pattern to ensure correct extraction of max salary
pattern = r'\$(\d+)K-\$(\d+)K'

# Use custom function to extract salary range
def extract_salaries(salary_str):
    match = re.search(pattern, salary_str)
    if match:
        min_salary = int(match.group(1)) * 1000
        max_salary = int(match.group(2)) * 1000
        return pd.Series([min_salary, max_salary])
    return pd.Series([0, 0])


cleaned_df[['Min Salary', 'Max Salary']] = cleaned_df['Salary Estimate'].apply(extract_salaries)
#print(cleaned_df[['Min Salary', 'Max Salary']] .head(5))
# Drop the original column if no longer needed
cleaned_df = cleaned_df.drop('Salary Estimate', axis=1)
# print(cleaned_df[['Min Salary', 'Max Salary']] .head(5))


#Correlation Analysis Cleaning
numeric_data = cleaned_df.select_dtypes(include=['number'])  # Separate numeric columns
categorical_data = cleaned_df.select_dtypes(exclude=['number'])  # Separate categorical columns
print(categorical_data)
numeric_columns = numeric_data.columns
categorical_columns = categorical_data.columns
print(categorical_columns)

correlation_matrix = numeric_data.corr()
plt.figure(figsize=(10, 8))  # Adjust the figure size
sns.heatmap(
    correlation_matrix,
    annot=True,  # Show correlation values
    fmt=".2f",  # Limit to 2 decimal places
    cmap="coolwarm",  # Color map
    cbar_kws={'label': 'Correlation'},  # Add label to the color bar
    linewidths=0.5,  # Add space between cells
)

# Title and labels
plt.title("Correlation Heatmap", fontsize=16)
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("../assets/scatter_matrix_heatmap.png")  # Save the figure as an image
plt.close()  # Close the figure to free memory
#plt.show()

# add new variables
cleaned_df['Salary Range'] = cleaned_df['Max Salary'] - cleaned_df['Min Salary']
cleaned_df['Salary Average'] = (cleaned_df['Max Salary'] + cleaned_df['Min Salary']) / 2
numeric_data = cleaned_df.select_dtypes(include=['number'])
#print(numeric_data)
correlation_matrix = numeric_data.corr()
plt.figure(figsize=(10, 8))  # Adjust the figure size
sns.heatmap(
    correlation_matrix,
    annot=True,  # Show correlation values
    fmt=".2f",  # Limit to 2 decimal places
    cmap="coolwarm",  # Color map
    cbar_kws={'label': 'Correlation'},  # Add label to the color bar
    linewidths=0.5,  # Add space between cells
)

# Title and labels
plt.title("Correlation Heatmap", fontsize=16)
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("../assets/scatter_matrix_heatmap_adjusted.png")  # Save the figure as an image
plt.close()
# plt.show()

#check if Location and Headquarters are highly correlated
# Check how often Location matches Headquarters
overlap_percentage = (data['Location'] == data['Headquarters']).mean() * 100
print(f"Percentage of overlap: {overlap_percentage:.2f}%")
# Create a cross-tabulation
crosstab = pd.crosstab(data['Location'], data['Headquarters'])
print(crosstab)

# Save the cleaned data to a CSV file
csv_path = '../Data/cleaned_data.csv'
cleaned_df.to_csv(csv_path, index=False)


