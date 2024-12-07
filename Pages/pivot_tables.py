from dash import html, dcc, callback, Output, Input, State, Patch
import dash
import pandas as pd
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/pivot_tables")

data = pd.read_csv("./Data/cleaned_data.csv",index_col=0)


# Step 1: Calculate Total Observations for each Industry
filtered_data = data[data['Industry'] != 'Unknown']
total_observations = filtered_data.groupby("Industry").size()

# Step 2: Calculate Average Rating for each Industry
average_rating = filtered_data.groupby("Industry")["Rating"].mean()

# Step 3: Extract Industry Names
industry_names = total_observations.index  # This gives the unique industry names

# Step 4: Combine results into a new DataFrame
result = pd.DataFrame({
    "Industry": industry_names,
    "Total Observations": total_observations.values,
    "Average Rating": average_rating.values
})

# Display the results
# print(result)
columnDefs = [{"field": i} for i in result.columns]

layout = dbc.Container([
                        html.Div([
                            dbc.Row([
                                    dcc.Input(id="quick-filter-input-3", placeholder="filter...")
                                    ],className='mb-3'),
                                    html.Hr(),
                            dbc.Row([
                                    dag.AgGrid(
                                                id="quick-filter-simple-3",
                                                columnDefs=columnDefs,
                                                rowData=result.to_dict("records"),
                                                defaultColDef={"filter": True},
                                                dashGridOptions={"pagination": True,
                                                                 "paginationPageSize": 10,
                                                                 "paginationPageSizeSelector": False,
                                                                 "animateRows": False,
                                                                 'cacheQuickFilter': True,
                                                                 "rowSelection":"single"},
                                                style={"height": "500px", "width": "100%"},  # Adjust table height and width
                                                )

                                    ],className='mb-3')
                                ])
                        ])

@callback(
    Output("quick-filter-simple-3", "dashGridOptions"),
    Input("quick-filter-input-3", "value"))


def update_filter(filter_value):
    newFilter = Patch()
    newFilter['quickFilterText'] = filter_value
    return newFilter