import plotly.express as px
import pandas as pd
import os

data = pd.read_csv("../Data/cleaned_data.csv")
print("Salary Estimate Columns:",data.columns.tolist())

# List of Top Data Analyst roles based on observations
roles =  ["Data Analyst",
    "Senior Data Analyst",
    "Junior Data Analyst",
    "Business Data Analyst",
    "Data Analyst II",
    "Data Quality Analyst",
    "Data Governance Analyst",
    "Lead Data Analyst",
    "Data Reporting Analyst",
    "Financial Data Analyst",
          ]


data = data[data["Job Title"].isin(roles)]
# print(data)
data['State'] = data['Location'].apply(lambda x: x.split(", ")[-1])
data['Founded Period'] = data['Founded'].apply(lambda x: 'Before 2000' if x < 2000 else 'After 2000')
# df=data.groupby('Location')[['Max Salary','Min Salary']].mean().sort_values(['Max Salary','Min Salary'],ascending=False).head(10)
# Filter the data to include only companies founded before 2000 or after 2000
before_after_new_df = data[data['Founded Period'] == 'After 2000']

df=before_after_new_df.groupby(['Job Title','Founded Period'])[['Max Salary','Min Salary']].mean().sort_values(['Max Salary','Min Salary'],ascending=False).head(10)
df = df.reset_index()
print(df)

# Reshape the data to long format for Plotly Express

longform_df = df.melt(id_vars=["Job Title"],
                        value_vars=['Min Salary', 'Max Salary'],
                        var_name='Salary Type',
                        value_name='Salary')



# # Group and aggregate
# df_grouped = longform_df.groupby(['Location', 'Salary Type'], as_index=False)['Salary'].sum()
# df_grouped = df_grouped.drop_duplicates()
# Create the stacked bar chart
fig = px.bar(
    longform_df,
    x='Job Title',
    y='Salary',
    color='Salary Type',
    barmode='stack',  # Stacked bar chart
    title='Top 10 Minimum and Maximum Salaries by Roles After 2000',
    color_discrete_sequence=['#deebf7', '#3182bd']  # Select two shades of blue  # Use the Blues range for colors
)

# Customize layout
fig.update_layout(
    xaxis_title='Job Title',
    yaxis_title='Salary($)',
    legend_title='Salary Type',
    template='plotly_dark',  # Dark theme
    height=600,
    title_font_size=20
)

# Show the chart
fig.write_image(os.path.join("../assets", "top_10_roles_mix_max_salary_after_2000.png"))
fig.show()