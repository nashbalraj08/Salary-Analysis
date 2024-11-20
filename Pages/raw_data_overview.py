from dash import Dash, dcc, html, Input, Output, callback,Patch
import plotly.express as px
import dash
import dash_ag_grid as dag
import pandas as pd

dash.register_page(__name__, "/raw_data_overview")

df = px.data.tips()
days = df.day.unique()

data = pd.read_csv("./Data/DataAnalyst.csv")
print(data)
numeric_data = data.select_dtypes(include=['number'])   # Separate numeric columns
categorical_data = data.select_dtypes(exclude=['number'])   # Separate categorical columns
numeric_columns = numeric_data.columns
categorical_columns = categorical_data.columns

numeric_stats = numeric_data.describe().transpose() # Descriptive statistics for numeric columns
numeric_stats.reset_index(inplace=True)
numeric_stats.rename(columns={'index': 'Numeric Predictor'}, inplace=True)
# print(numeric_stats)

categorical_stats = categorical_data.describe().transpose()
categorical_stats.reset_index(inplace=True)
categorical_stats.rename(columns={'index': 'Categorical Predictor'}, inplace=True)
columnDefs = [{"field": i} for i in data.columns]


#count how many whitespaces in each column
whitespace_counts = data.apply(lambda col: col.map(lambda x: isinstance(x, str) and x.strip() == "").sum())
# Store results in a new DataFrame
whitespace_summary = pd.DataFrame({
    "Column": whitespace_counts.index,
    "Whitespace Count": whitespace_counts.values
})
#print(whitespace_summary)

# Generate a DataFrame with missing value counts
missing_values = data.isnull().sum().reset_index()
missing_values.columns = ['Column', 'Missing Values']
missing_values_columns = [{'field':i} for i in missing_values.columns]
#print(missing_values)

# Define a function to count special characters in a column
def count_special_characters(col):
    return col.map(lambda x: sum(1 for c in str(x) if not c.isalnum()) if isinstance(x, str) else 0).sum()

# Count special characters for each column
special_char_counts = data.apply(count_special_characters)

# Store results in a new DataFrame
special_char_summary = pd.DataFrame({
    "Column": special_char_counts.index,
    "Special Character Count": special_char_counts.values
})
#print(special_char_summary)

# Identify duplicate rows
duplicate_rows = data[data.duplicated(keep=False)]  # Get all duplicate rows, including the first occurrence
duplicate_count = duplicate_rows.shape[0]  # Count duplicate rows

# Store the results in a DataFrame
duplicates_summary = pd.DataFrame({
    "Total Rows": [data.shape[0]],
    "Duplicate Rows": [duplicate_count],
    "Unique Rows": [data.shape[0] - duplicate_count]
})
#print(duplicates_summary)

layout = html.Div(
    [
        dcc.Markdown("Raw Data Table Overview"),
        dcc.Input(id="quick-filter-input", placeholder="filter..."),
        dag.AgGrid(
            id="quick-filter-simple",
            columnDefs=columnDefs,
            rowData=data.to_dict("records"),
            defaultColDef={"filter": True},
            dashGridOptions={"pagination": True,
                             "paginationPageSize": 10,
                             "paginationPageSizeSelector": False,
                             "animateRows": False,
                             'cacheQuickFilter': True,
                             "rowSelection":"single"},
        )
    ]
)


@callback(
    Output("quick-filter-simple", "dashGridOptions"),
    Input("quick-filter-input", "value"))

def update_filter(filter_value):
    newFilter = Patch()
    newFilter['quickFilterText'] = filter_value
    return newFilter
