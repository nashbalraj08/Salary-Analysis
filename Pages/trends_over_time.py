from dash import html, dcc, callback, Output, Input, State
import dash
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/trends-over-time")


layout = html.H1("Trends over time")

# data = {
#     "Month-Year": [
#         "2022-11", "2022-12", "2023-01", "2023-02", "2023-03",
#         "2023-04", "2023-05", "2023-06", "2023-07", "2023-08",
#         "2023-09", "2023-10"
#     ],
#     "Frequency": [1000, 1250, 1500, 1800, 1700, 1400, 1300, 1200, 1350, 1550, 1600, 200]
# }
# data = pd.DataFrame(data)
# # avg_salary = data.groupby("via", as_index=False)["salary"].mean()

data = pd.read_csv("./Data/cleaned_data.csv",index_col=0)

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
        ]),
        dbc.Col([
            html.H5("Choose your y-axis value:"),
            dcc.Dropdown(
                        id="y-dropdown",
                        options=numeric_columns,
                        multi=False,
                        value=numeric_columns[1]
                    )

        ],width=6)
        ],className='mb-3'),
        dbc.Row([
        dbc.Button('Update Graph', id='my-button', n_clicks=0, style={"width": "100%"}),
        ],className='mb-3'),
        dbc.Row([
        dcc.Graph(id="line-chart")
        ],className='mb-3')

    ])

])

@callback(
    Output("line-chart", "figure"),
    Input('my-button','n_clicks'),
    State("x-dropdown", "value"),
    State("y-dropdown", "value")
)
def update_line_chart(clicks,x_dropdown, y_dropdown):
    sector_avg_rating = data.groupby(x_dropdown)[y_dropdown].mean().sort_index()
    cleaned_df = sector_avg_rating.reset_index()
    line_chart = px.line(
        cleaned_df,
        x=x_dropdown,
        y=y_dropdown,
        title="Trends Over Time"
    )
    # Apply dark theme
    line_chart.update_layout(
        template="plotly_dark",
        xaxis_title=f"{x_dropdown}",
        yaxis_title=f"{y_dropdown}",
        title=dict(x=0.5),  # Center the title
        font=dict(size=12)
    )

    return line_chart