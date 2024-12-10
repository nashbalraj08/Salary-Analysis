import pandas as pd
import numpy as np
data2 = pd.read_csv("../Data/DataAnalyst.csv", index_col=0)
data3 = data2[['Company Name','Rating']]
data3.replace(-1, np.nan, inplace=True)
print(data3)
print(data3['Rating'].sample(10))
print(data3['Rating'].isnull().sum())
# Filter rows where the Rating column is null
filtered_df = data3[data3['Rating'].isnull()][['Company Name', 'Rating']]
# Split the "Company Name" column by '\r\n' and extract the numeric part
filtered_df['Rating Number'] = filtered_df['Company Name'].str.split(r'\r\n').str[0]
print(filtered_df.tail(10))
filtered_df = filtered_df[['Rating Number','Rating']]
print(filtered_df.head(100))
