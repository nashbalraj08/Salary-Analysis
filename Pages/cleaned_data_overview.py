from dash import Dash, dcc, html, Input, Output, callback,Patch
import dash_bootstrap_components as dbc
import plotly.express as px
import dash
import dash_ag_grid as dag
import pandas as pd

dash.register_page(__name__, "/data-cleaned")

df = px.data.tips()
days = df.day.unique()

data = pd.read_csv("./Data/cleaned_data.csv",index_col=0)
# print(data)
data = data.reset_index()
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

# Create a DataFrame to store unique values for each column
unique_values_all_df = pd.DataFrame({
    "Column Name": data.columns,
    "Unique Count": [data[col].nunique() for col in data.columns],
    "Unique Values": [data[col].unique().tolist() for col in data.columns]
})


layout = html.Div(
    [
        dbc.Row([
        dcc.Markdown("Clean Data Table Overview",style={"textAlign": "center"})],className='mb-3'),

        dbc.Row([
        dcc.Input(id="quick-filter-input-clean", placeholder="filter...")
        ],className='mb-3'),
        html.Hr(),
        dbc.Row([
            dag.AgGrid(
            id="quick-filter-simple-clean",
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
        ],className='mb-3'),
        dbc.Row([
            dcc.Markdown("Descriptive Stats Table Overview")
        ]),
        dbc.Row([
            dag.AgGrid(id="grid-clean",
                       rowData=numeric_stats.to_dict("records"),
                       columnDefs=[{"field":i} for i in numeric_stats.columns],
                       dashGridOptions={"rowSelection":"single"})

        ]),
        html.Hr(),
        dbc.Row([
            dcc.Markdown("Categorical Stats Table Overview")
        ]),
        dbc.Row([
            dag.AgGrid(id="categorical-grid-clean",
                       rowData=categorical_stats.to_dict("records"),
                       columnDefs=[{"field": i} for i in categorical_stats.columns],
                       dashGridOptions={"rowSelection": "single"})
        ]),
        html.Hr(),
        dbc.Row([
            dcc.Markdown("Whitespaces in each column")
        ]),
        dbc.Row([
            dag.AgGrid(id="categorical-grid-2-clean",
                       rowData=whitespace_summary.to_dict("records"),
                       columnDefs=[{"field": i} for i in whitespace_summary.columns],
                       dashGridOptions={"rowSelection": "single"})
        ]),
        html.Hr(),
        dbc.Row([
            dcc.Markdown("Empty Values in each column")
        ]),
        dbc.Row([
            dag.AgGrid(id="categorical-grid-3-clean",
                       rowData=missing_values.to_dict("records"),
                       columnDefs=[{"field": i} for i in missing_values.columns],
                       dashGridOptions={"rowSelection": "single"})
        ]),
        html.Hr(),
        dbc.Row([
            dcc.Markdown("Special Characters in each column")
        ]),
        dbc.Row([
            dag.AgGrid(id="categorical-grid-4-clean",
                       rowData=special_char_summary.to_dict("records"),
                       columnDefs=[{"field": i} for i in special_char_summary.columns],
                       dashGridOptions={"rowSelection": "single"})
        ]),
        html.Hr(),
        dbc.Row([
            dcc.Markdown("Total Duplicates")
        ]),
        dbc.Row([
            dag.AgGrid(id="categorical-grid-5-clean",
                       rowData=duplicates_summary.to_dict("records"),
                       columnDefs=[{"field": i} for i in duplicates_summary.columns],
                       dashGridOptions={"rowSelection": "single","paginationPageSize": 1})
        ]),
        html.Hr(),
        dbc.Row([
            dcc.Markdown("Unique Values")
        ]),
        dbc.Row([
            dag.AgGrid(id="unique-values-table-clean",
                        columnDefs=[{"field": i} for i in unique_values_all_df.columns],
                        rowData=unique_values_all_df.to_dict("records"),
                        defaultColDef={"filter": True},
                        dashGridOptions={"pagination": True,
                                         "paginationPageSize": 10,
                                         "paginationPageSizeSelector": False,
                                         "animateRows": False,
                                         'cacheQuickFilter': True,
                                         "rowSelection":"single"}
            ),
        ])
    ])


@callback(
    Output("quick-filter-simple-clean", "dashGridOptions"),
    Input("quick-filter-input-clean", "value"))

def update_filter_2(filter_value):
    newFilter = Patch()
    newFilter['quickFilterText'] = filter_value
    return newFilter
