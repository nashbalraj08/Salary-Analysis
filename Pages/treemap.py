import plotly.express as px
import pandas as pd
import os

data2 = pd.read_csv("../Data/cleaned_data.csv",index_col=0)
data2['State'] = data2['Location'].apply(lambda x: x.split(", ")[-1])
data2['Founded Period'] = data2['Founded'].apply(lambda x: 'Before 2000' if x < 2000 else 'After 2000')
data2 = data2[data2['Industry'] != 'Unknown']
# before_after_new_df = data2[data2['Founded Period'] == 'After 2000']
company_counts = data2.groupby(["Industry", "State","Founded Period"]).size()
# Step 3: Extract Industry Names
industry_states = company_counts.index  # This gives a MultiIndex (Company Name, State, Founded Period)
# Step 4: Combine results into a new DataFrame
result3 = pd.DataFrame({
    "Industry Name": [index[0] for index in industry_states],  # Extract Company Name from MultiIndex
    "State": [index[1] for index in industry_states],
    "Founded Period": [index[2] for index in industry_states], # Extract Founded Period from MultiIndex# Extract State from MultiIndex,
    "Total Observations": company_counts.values,
})

fig = px.treemap(
    result3,
    path=["Founded Period", "State", "Industry Name"],  # Drill down by time period, state, and industry
    values="Total Observations",                       # Size of each rectangle based on company count
    color="Industry Name",                             # Color by industry
    title="Industry Distribution by State Before and After 2000",
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig.update_layout(template="plotly_dark")
fig.write_image(os.path.join("../assets", "treemap_before_after_2000.png"))
fig.show()