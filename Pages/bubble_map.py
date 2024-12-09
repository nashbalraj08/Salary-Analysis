import plotly.express as px
import pandas as pd
import os

data2 = pd.read_csv("../Data/cleaned_data.csv",index_col=0)

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

# Step 1: Aggregate the data for bubble size
bubble_data = (
    before_after_new_df.groupby(["State", "Industry Name"])["Total Observations"]
    .sum()
    .reset_index()
)

# Step 2: Create a Bubble Map
fig = px.scatter_geo(
    bubble_data,
    locations="State",
    locationmode="USA-states",
    size="Total Observations",           # Bubble size indicates the count
    color="Industry Name",               # Color by industry
    scope="usa",
    title="Industry Distribution Across States After 2000",
    hover_name="Industry Name",          # Hover for more details
    template="plotly_dark"
)

# Display the map
fig.show()