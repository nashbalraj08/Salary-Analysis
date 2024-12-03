
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time


data = pd.read_csv("../Data/cleaned_data.csv",index_col=0)
# print(data)
numeric_data = data.select_dtypes(include=['number'])  # Separate numeric columns
categorical_data = data.select_dtypes(exclude=['number'])  # Separate categorical columns
numeric_columns = numeric_data.columns
categorical_columns = categorical_data.columns

#For Categorical Data Encoding: convert them into numeric using encoding techniques (one-hot encoding):
selected_columns = ['Type of ownership','Sector','Size']  # Replace with your column names
dummies = pd.get_dummies(categorical_data[selected_columns], drop_first=True)
# print(dummies.corr())
correlation_matrix = dummies.corr()
# plt.figure(figsize=(20, 16))  # Adjust the figure size
# sns.heatmap(
#     filtered_corr,
#     annot=True,  # Show correlation values
#     fmt=".2f",  # Limit to 2 decimal places
#     cmap="coolwarm",  # Color map
#     cbar_kws={'label': 'Correlation'},  # Add label to the color bar
#     linewidths=0.5,  # Add space between cells
# )
#
# # Title and labels
# plt.title("Correlation Heatmap", fontsize=8)
# plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels
# plt.yticks(rotation=0)
# plt.tight_layout()
# plt.savefig("C:/Users/Nash Balraj/PycharmProjects/salaryAnalysis/assets/scatter_matrix_heatmap_categorical.png")  # Save the figure as an image
# # plt.close()
# plt.show()

def matrix_heatmap(data, save_directory="../assets" ):
    plt.figure(figsize=(20, 16))  # Adjust the figure size
    sns.heatmap(
        data,
        annot=True,  # Show correlation values
        fmt=".2f",  # Limit to 2 decimal places
        cmap="coolwarm",  # Color map
        cbar_kws={'label': 'Correlation'},  # Add label to the color bar
        linewidths=0.5,  # Add space between cells
    )

    # Title and labels
    plt.title("Correlation Heatmap", fontsize=8)
    plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels
    plt.yticks(rotation=0)
    plt.tight_layout()

    # Generate a timestamped filename
    timestamp = time.strftime("%Y%m%d-%H%M%S")  # Format: YYYYMMDD-HHMMSS
    filename = f"{save_directory}/heatmap_{timestamp}.png"

    # Save the figure
    plt.savefig(filename)
    plt.close()  # Close the plot to free memory
    return filename


# Call the function
matrix_heatmap(correlation_matrix)

#Adjust threshold
threshold = 0.7
filtered_corr = correlation_matrix[(correlation_matrix > threshold) | (correlation_matrix < -threshold)]
matrix_heatmap(filtered_corr)

# Drop one of the correlated variables
adjusted_corr = dummies.drop(columns=['Sector_Government'])
matrix_heatmap(adjusted_corr)