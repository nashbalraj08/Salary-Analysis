import os
import pandas as pd
import plotly.express as px

# # Sample Dataset
# data = {
#     'Company Name': ['Company A', 'Company B', 'Company C', 'Company D', 'Company E'],
#     'Founded Year': [1998, 2005, 2010, 1995, 2018],
#     'Rating': [3.5, 4.2, 4.8, 3.0, 4.5]
# }
# # Create DataFrame
# df = pd.DataFrame(data)

df = pd.read_csv("../Data/cleaned_data.csv",index_col=0)
df = df.reset_index()
# Categorize Time Periods
df['Time Period'] = df['Founded'].apply(lambda x: 'Before 2000' if x < 2000 else 'After 2000')

# Top 10 Industry Salary ranges
top_10_industries = [
    "IT Services", "Staffing & Outsourcing", "Enterprise Software & Network Solutions",
    "Internet", "Health Care Services & Hospitals", "Consulting",
    "Computer Hardware & Software", "Advertising & Marketing",
    "Banks & Credit Unions", "Investment Banking & Asset Management"
]

df = df[df["Industry"].isin(top_10_industries)]
df['Founded Period'] = df['Founded'].apply(lambda x: 'Before 2000' if x < 2000 else 'After 2000')
# Filter the data to include only companies founded before 2000 or after 2000
before_after_new_df = df[df['Founded Period'] == 'Before 2000']

def update_boxplot(x,y):
    boxplot = px.box(before_after_new_df,
                     x=x,
                     y=y,
                     title="Comparison of Data Analyst Salary Before 2000",
                     points="all",
                     color="Industry")
    boxplot.update_layout(template='plotly_dark',
                          xaxis_title="Industry",
                          yaxis_title="Salary($)"
                          )
    # boxplot.write_image(os.path.join("../assets", "boxplot_salary_industry_before_2000.png"))
    # boxplot.show()

    return "boxplot display in runtime environment"

# update_boxplot('Time Period','Rating')
# update_boxplot('Industry','Salary Midpoint')



def update_boxplot_histogram(x_axis):
    combo = px.histogram(df,
                     x= x_axis,
                     title="Average Salary Distribution",
                     marginal="box",
                     hover_data = df[['Job Title', 'Company Name']])
    combo.update_layout(template='plotly_dark',
                          xaxis_title="Average Salary($)",
                          yaxis_title="Count"
                          )

    combo.write_image(os.path.join("../assets", "average_salary_distribution.png"))
    combo.show()
    return "boxplot_histogram display in runtime environment"

update_boxplot_histogram('Salary Average')


