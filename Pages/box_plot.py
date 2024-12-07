
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

# Categorize Time Periods
df['Time Period'] = df['Founded'].apply(lambda x: 'Before 2000' if x < 2000 else 'After 2000')


def update_boxplot(x,y):
    boxplot = px.box(df,
                     x=x,
                     y=y,
                     title="Comparison of Company Ratings Before and After 2000",
                     points="all",
                     color="Time Period")
    boxplot.update_layout(template='plotly_dark')
    boxplot.show()

    return "boxplot display in runtime environment"

update_boxplot('Time Period','Rating')