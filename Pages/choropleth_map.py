import plotly.express as px
import pandas as pd
import os


data2 = pd.read_csv("../Data/cleaned_data.csv",index_col=0)

#Location vs Distribution of Companies and Salary
# Step 1: Extract the state from the 'Location' column
data2['State'] = data2['Location'].apply(lambda x: x.split(", ")[-1])

# Step 2: Filter out rows where 'State' or 'Founded' is unknown
filtered_data = data2[data2['State'] != 'Unknown']
filtered_data = filtered_data[filtered_data['Founded'] != 'Unknown']

# Step 3: Add a new column to categorize companies into 'Before 2000' or 'After 2000'
filtered_data['Founded Period'] = filtered_data['Founded'].apply(lambda x: 'Before 2000' if x < 2000 else 'After 2000')

# Step 4: Group data by State and Founded Period, and count companies
company_counts = filtered_data.groupby(['State', 'Founded Period'])['Company Name'].size().reset_index()
# Step 4b: Calculate Average Salary Range for each Company Name in each state
state_salary = filtered_data.groupby(['State', 'Founded Period'])["Salary Midpoint"].mean().reset_index()
# print(state_salary)
# Rename the columns for clarity
company_counts.columns = ['State', 'Founded Period', 'Total Companies']
# print(company_counts)





#States vs Distribution of Dominate Top 10 Industries
# Step 1: Define the top 10 industries
top_10_industries = [
    "IT Services", "Staffing & Outsourcing", "Enterprise Software & Network Solutions",
    "Internet", "Health Care Services & Hospitals", "Consulting",
    "Computer Hardware & Software", "Advertising & Marketing",
    "Banks & Credit Unions", "Investment Banking & Asset Management"
]

# Step 1: Extract the state from the 'Location' column
data2['State'] = data2['Location'].apply(lambda x: x.split(", ")[-1])
data2['Founded Period'] = data2['Founded'].apply(lambda x: 'Before 2000' if x < 2000 else 'After 2000')
data2 = data2[data2["Industry"].isin(top_10_industries)]

# Step 1: Calculate Total Observations for each Company
filtered_data = data2[data2['Industry'] != 'Unknown']
total_observations = filtered_data.groupby(["Industry", "State","Founded Period"]).size()

# Step 2: Calculate Average Salary Range for each Company Name
average_salary = filtered_data.groupby(["Industry", "State","Founded Period"])["Salary Range"].mean()

# Step 3: Extract Industry Names
industry_states = total_observations.index  # This gives a MultiIndex (Company Name, State, Founded Period)


# Step 4: Combine results into a new DataFrame
result3 = pd.DataFrame({
    "Industry Name": [index[0] for index in industry_states],  # Extract Company Name from MultiIndex
    "State": [index[1] for index in industry_states],
    "Founded Period": [index[2] for index in industry_states], # Extract Founded Period from MultiIndex# Extract State from MultiIndex,
    "Total Observations": total_observations.values,
    "Salary Range": average_salary.values
})
# print(result3)
# print(result3.nlargest(10, "Total Observations"))# top 10 rated industries, filtered by industries with the highest total observations

# Filter the data to include only companies founded before 2000 or after 2000
before_after_new_df = result3[result3['Founded Period'] == 'After 2000']

# Step 1: Aggregate to find the dominant industry in each state for After 2000
dominant_industries = (
    before_after_new_df.groupby(["State", "Industry Name"])["Total Observations"]
    .sum()
    .reset_index()
)
print(dominant_industries)

# Step 2: Identify the most dominant industry in each state
dominant_industry_per_state = (
    dominant_industries.loc[dominant_industries.groupby("State")["Total Observations"].idxmax()]
)
print(dominant_industry_per_state)

# Create a Choropleth Map for companies
fig = px.choropleth(
    dominant_industry_per_state,
    locations="State",               # Column with states names
    locationmode="USA-states",      # Match country names to map
    color="Industry Name",  # Column for color intensity
    scope="usa",  # Restrict to the USA
    title="Dominance of Industries After 2000",
    color_continuous_scale="Blues"     # Color scale
)

# Update layout for a better look
fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type="albers usa" # Focus on US map

    ),
    coloraxis_colorbar=dict(
            title= "Type of Industry",
            ticktext=['Low', 'High']
        ),

    template="plotly_dark"
)

# Display the map
# Save the figure as an image
fig.write_image(os.path.join("../assets", "choropleth_map_industry_after_2000.png"))
fig.show()
