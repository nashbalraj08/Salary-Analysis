from dash import Dash, dcc, html, Input, Output, callback,Patch, State
import dash_bootstrap_components as dbc
import plotly.express as px
import dash
import numpy as np
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
dash.register_page(__name__, path="/top-bottom-10")


data = {
    "via": ["Via A", "Via B", "Via C", "Via D", "Via E", "Via F", "Via G", "Via H", "Via I", "Via J",
            "Via K", "Via L", "Via M", "Via N", "Via O", "Via P", "Via Q", "Via R", "Via S", "Via T"],
    "salary": [4000, 3500, 3200, 4500, 5000, 2800, 4200, 3900, 3000, 3100,
               3400, 4700, 5100, 2900, 4100, 4300, 3600, 3800, 3700, 4800]
}
data = pd.DataFrame(data)

numeric_data = data.select_dtypes(include=['number'])  # Separate numeric columns
categorical_data = data.select_dtypes(exclude=['number'])  # Separate categorical columns
numeric_columns = numeric_data.columns
categorical_columns = categorical_data.columns
# Set default values
x_axis = numeric_columns[0] if len(numeric_columns) > 0 else None  # First numeric column
y_axis = categorical_columns[0] if len(categorical_columns) > 0 else None  # First categorical column


layout =dbc.Container([
    html.Div([
        dbc.Row([
        dbc.Col([
            html.H5("Choose your x-axis value:"),
            dcc.Dropdown(
                        id="x-dropdown",
                        options=data.columns,
                        multi=False,
                        value=x_axis
                    )
        ],width=6),
        dbc.Col([
            html.H5("Choose your y-axis value:"),
            dcc.Dropdown(
                        id="y-dropdown",
                        options=data.columns,
                        multi=False,
                        value=y_axis
                    )

        ],width=6)
        ],className='mb-3'),
        dbc.Row([
            dbc.Col([
                html.H5("Choose top 10,bottom 10 or none:"),
                dcc.Dropdown(
                id="filter-dropdown",
                options=[
                    {"label": "Top 10", "value": "top"},
                    {"label": "Bottom 10", "value": "bottom"},
                    {"label": "None", "value": "none"}
                ],
                value="none",
                placeholder="Select a filter",
                style={"width": "50%", "margin": "auto"}
                )
            ],width=12)

        ]),
        dbc.Row([
        dbc.Button('Update Graph', id='my-button-3', n_clicks=0, style={"width": "100%"}),
        ],className='mb-3'),
        dbc.Row([
        dcc.Graph(id="bar-graph-3")
        ],className='mb-3')
    ])
])
@callback(
    Output("bar-graph-3", "figure"),
    Input('my-button-3','n_clicks'),
    State("x-dropdown", "value"),
    State("y-dropdown", "value"),
    State("filter-dropdown","value")
)

def update_bar_graph(clicks,x_dropdown, y_dropdown,top_bottom):
    if top_bottom == "top":
        filtered_df = data.nlargest(10, "salary")  # Top 10
    elif top_bottom == "bottom":
        filtered_df = data.nsmallest(10, "salary")  # Bottom 10
    else:
        filtered_df = data
    bar_graph_2 = px.bar(
        filtered_df,
        x="via",
        y="salary",
        color="salary",
        color_continuous_scale="Blues",  # Reverse Blues color scale
        title="Bar Chart with Color Scale",
        labels={"salary": "salary"},
        category_orders={"via": data.sort_values("salary", ascending=False)["via"].tolist()}
        # Sort in descending order
    )
    # Update layout
    bar_graph_2.update_layout(
        template="plotly_dark",  # Dark theme
        xaxis_title="via",
        yaxis_title="salary",
        coloraxis_colorbar=dict(
            title="salary",
            tickvals=np.linspace(data['salary'].min(), data['salary'].max(),num=3),
            ticktext=["low", "medium", "high"]
        ))
    return bar_graph_2
