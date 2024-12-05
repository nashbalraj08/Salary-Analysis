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


# data = pd.DataFrame({
#     'Sectors': ['Information Technology', 'Business Services', 'Finance',
#                 'Health Care', 'Education', 'Insurance',
#                 'Accounting & Legal', 'Media', 'Manufacturing', 'Retail'],
#     'Rating': [4.5, 4.2, 3.9, 4.0, 3.5, 3.8, 3.2, 3.0, 3.6, 2.8],
#     'Count': [550, 450, 350, 300, 200, 150, 120, 100, 90, 80]
# })

data = pd.read_csv("./Data/cleaned_data.csv",index_col=0)

cleaned_df = data.copy()


# # Get the top 10 sectors based on ratings
# sector_avg_rating = cleaned_df.groupby('Sector')['Rating'].mean().sort_values(ascending=True)
#
# top_10_sectors = pd.DataFrame(sector_avg_rating).tail(10)
# bottom_10_sectors = pd.DataFrame(sector_avg_rating).head(10)
#
# # rating_df = top_10_sectors.reset_index()
# rating_df = bottom_10_sectors.reset_index()

def top_bottom_10(df, groupby_var, measurement_var, top_bottom=10, order="Top"):
    # Group by the specified variable and calculate the average of the measurement variable
    grouped_avg = df.groupby(groupby_var)[measurement_var].mean().sort_values(ascending=True)
    # Select top or bottom N groups
    if order == "Top":
        result = grouped_avg.tail(top_bottom)
    elif order == "Bottom":
        result = grouped_avg.head(top_bottom)
    else:
        raise ValueError("The 'order' parameter must be 'top' or 'bottom'.")

    # Convert the result into a DataFrame and reset the index
    result_df = result.reset_index()

    return result_df

# bottom_10_sectors = top_bottom_10(data, 'Sector', 'Rating', 10, "bottom")



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
                        options=numeric_columns,
                        multi=False,
                        value=x_axis
                    )
        ],width=6),
        dbc.Col([
            html.H5("Choose your y-axis value:"),
            dcc.Dropdown(
                        id="y-dropdown",
                        options=categorical_columns,
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
                    {"label": "Top 10", "value": "Top"},
                    {"label": "Bottom 10", "value": "Bottom"}
                ],
                value="Top",
                placeholder="Select a filter",
                style={"width": "50%", "margin": "auto"}
                )
            ],width=12)

        ]),
        html.Hr(),
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

def update_bar_chart(clicks,x_axis,y_axis,top_bottom):

    # Create bar chart with Plotly Express
    bottom_10_sectors = top_bottom_10(data, y_axis, x_axis, 10, top_bottom)
    fig = px.bar(
        bottom_10_sectors,
        x=x_axis,
        y=y_axis,
        color=x_axis,
        orientation='h',  # Horizontal bars
        color_continuous_scale='Viridis_r', #Blues_r
        range_color=(bottom_10_sectors[x_axis].min(), bottom_10_sectors[x_axis].max()),  # scale
        title= f"{top_bottom} 10 {y_axis} by {x_axis}"
    )

    # Customize layout
    fig.update_layout(
        height=600,
        title_font_size=20,
        xaxis_title= f"{x_axis}",
        yaxis_title= f"{y_axis}",
        coloraxis_colorbar=dict(
            title= f"{x_axis}",
            tickvals=[bottom_10_sectors[x_axis].min(), bottom_10_sectors[x_axis].max()],
            ticktext=['Low', 'High']
        ),
        template="plotly_dark"  # Dark theme
    )

    return fig

