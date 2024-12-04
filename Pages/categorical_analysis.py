import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time



data = pd.read_csv("../Data/cleaned_data.csv", index_col=0)
# print(data)

# Find the most common categories

# Filter out the rows where 'Industry' is 'unknown'
filtered_data = data[data['Industry'] != 'Unknown']
# Calculate the value counts for the filtered dataset
industry_counts = filtered_data['Industry'].value_counts()


company_name_counts = data['Company Name'].value_counts()

# Filter out the rows where 'Industry' is 'unknown'
filtered_data = data[data['Headquarters'] != 'Unknown']
headquarters_counts = filtered_data['Headquarters'].value_counts()


location_counts = data['Location'].value_counts()

# Filter out the rows where 'Industry' is 'unknown'
filtered_data = data[data['Sector'] != 'Unknown']
sector_counts = filtered_data['Sector'].value_counts()

# Display the top 10 most common
# print(industry_counts.head(10))
# print(company_name_counts.head(10))
# print(headquarters_counts.head(10))
# print(location_counts.head(10))
# print(sector_counts.head(10))


# Plot the top 10 industries
plt.figure(figsize=(10, 6))
sns.barplot(x=sector_counts.head(10).values, y=sector_counts.head(10).index, palette="Blues_r")
plt.title("Top 10 Most Common Sectors", fontsize=16)
plt.xlabel("Count")
plt.ylabel("Sectors")
plt.tight_layout()
plt.savefig("../assets/Top_10_Most_Common_Sectors.png")  # Save the figure as an image
plt.close()
