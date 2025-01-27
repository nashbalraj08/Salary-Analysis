import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time



data = pd.read_csv("../Data/cleaned_data.csv", index_col=0)
data = data.reset_index()
# # print(data)
#
# sector_avg_rating = data.groupby('Founded')['Rating'].mean().sort_values(ascending=False)
# print(type(sector_avg_rating))
# cleaned_df = sector_avg_rating.reset_index()
# print(cleaned_df)

# bottom_10_sectors = pd.DataFrame(sector_avg_rating).tail(10)
# print(type(bottom_10_sectors))
# print(bottom_10_sectors)
# cleaned_df = bottom_10_sectors.reset_index()
# print(cleaned_df)
#
# # # Get the top 10 sectors based on ratings
# # sector_avg_rating = cleaned_df.groupby('Sector')['Rating'].mean().sort_values(ascending=True)
# #
# # top_10_sectors = pd.DataFrame(sector_avg_rating).tail(10)
# # bottom_10_sectors = pd.DataFrame(sector_avg_rating).head(10)
#
# # # rating_df = top_10_sectors.reset_index()
# # rating_df = bottom_10_sectors.reset_index()
#
# def top_bottom_10(df, groupby_var, measurement_var, top_bottom=10, order="top"):
#     # Group by the specified variable and calculate the average of the measurement variable
#     grouped_avg = df.groupby(groupby_var)[measurement_var].mean().sort_values(ascending=True)
#     # Select top or bottom N groups
#     if order == "top":
#         result = grouped_avg.head(top_bottom)
#     elif order == "bottom":
#         result = grouped_avg.tail(top_bottom)
#     else:
#         raise ValueError("The 'order' parameter must be 'top' or 'bottom'.")
#
#     # Convert the result into a DataFrame and reset the index
#     result_df = result.reset_index()
#
#     return result_df
#
# # Sample DataFrame
# # data = pd.DataFrame({
# #     'Sector': ['IT', 'Finance', 'Healthcare', 'Retail', 'IT', 'Finance', 'Healthcare', 'Retail'],
# #     'Rating': [4.5, 4.2, 3.9, 3.7, 4.8, 4.1, 4.0, 3.5]
# # })
#
# # Get top 10 sectors by average rating
# top_10_sectors = top_bottom_10(data, 'Sector', 'Rating', 10, "top")
# print("Top 10 Sectors:")
# print(top_10_sectors)
# bottom_10_sectors = top_bottom_10(data, 'Sector', 'Rating', 10, "bottom")
# print("Bottom 10 Sectors:")
# print(bottom_10_sectors)
#
#
# # Find the most common categories
#
# Filter out the rows where 'Industry' is 'unknown'
filtered_data = data[data['Job Title'] != 'Unknown']
# Calculate the value counts for the filtered dataset
industry_counts = filtered_data['Job Title'].value_counts()
# #
# #
# # company_name_counts = data['Company Name'].value_counts()
# #
# # # Filter out the rows where 'Industry' is 'unknown'
# # filtered_data = data[data['Headquarters'] != 'Unknown']
# # headquarters_counts = filtered_data['Headquarters'].value_counts()
# #
# #
# # location_counts = data['Location'].value_counts()
# #
# # # Filter out the rows where 'Industry' is 'unknown'
# # filtered_data = data[data['Sector'] != 'Unknown']
# # sector_counts = filtered_data['Sector'].value_counts()
#
# # Get the top 10 sectors based on ratings
#
# # Display the top 10 most common
#
# # print(industry_counts.head(10))
# # print(company_name_counts.head(10))
# # print(headquarters_counts.head(10))
# # print(location_counts.head(10))
# # print(sector_counts.head(10))
#
#
# Plot the top 10 industries
plt.figure(figsize=(10, 6))
sns.barplot(x=industry_counts.head(10).values, y=industry_counts.head(10).index, palette="Blues_r")
plt.title("Top 10 Most Common Roles", fontsize=16)
plt.xlabel("Number of Observations")
plt.ylabel("Roles")
plt.tight_layout()
plt.savefig("../assets/Top_10_Most_Common_Roles.png")  # Save the figure as an image
plt.show()
plt.close()
