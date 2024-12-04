from dash import Dash, dcc, html, Input, Output, callback,Patch, State
import dash_bootstrap_components as dbc
import plotly.express as px
import dash
import dash_ag_grid as dag
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go


dash.register_page(__name__, "/data-exploration-visuals")


data = pd.read_csv("./Data/cleaned_data.csv",index_col=0)
# Define the path to the images directory




numeric_data = data.select_dtypes(include=['number'])  # Separate numeric columns
categorical_data = data.select_dtypes(exclude=['number'])  # Separate categorical columns
numeric_columns = numeric_data.columns
categorical_columns = categorical_data.columns
# Set default values
x_axis = numeric_columns[0] if len(numeric_columns) > 0 else None  # First numeric column
y_axis = categorical_columns[0] if len(categorical_columns) > 0 else None  # First categorical column
default_axis = data.columns[0] if len(data.columns) >0 else None


correlation_matrix = numeric_data.corr()
plt.figure(figsize=(10, 8))  # Adjust the figure size
sns.heatmap(
    correlation_matrix,
    annot=True,  # Show correlation values
    fmt=".2f",  # Limit to 2 decimal places
    cmap="coolwarm",  # Color map
    cbar_kws={'label': 'Correlation'},  # Add label to the color bar
    linewidths=0.5,  # Add space between cells
)

# Title and labels
plt.title("Correlation Heatmap", fontsize=16)
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("assets/scatter_matrix_heatmap.png")  # Save the figure as an image
plt.close()  # Close the figure to free memory
#plt.show()

# Correlation Analysis
# add new variables
data['Salary Range'] = data['Max Salary'] - data['Min Salary']
data['Salary Midpoint'] = (data['Max Salary'] + data['Min Salary']) / 2
numeric_data = data.select_dtypes(include=['number'])
#print(numeric_data)
correlation_matrix = numeric_data.corr()
plt.figure(figsize=(10, 8))  # Adjust the figure size
sns.heatmap(
    correlation_matrix,
    annot=True,  # Show correlation values
    fmt=".2f",  # Limit to 2 decimal places
    cmap="coolwarm",  # Color map
    cbar_kws={'label': 'Correlation'},  # Add label to the color bar
    linewidths=0.5,  # Add space between cells
)

# Title and labels
plt.title("Correlation Heatmap", fontsize=16)
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("assets/scatter_matrix_heatmap_adjusted.png")  # Save the figure as an image
plt.close()
# plt.show()

layout = dbc.Container([
    html.Div([
        dbc.Row([
            html.H1("Data Exploration")
        ],className='mb-3'),
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
        dbc.Button('Update Bar Graph', id='my-button', n_clicks=0, style={"width": "100%"})
        ],className='mb-3'),
        html.Div([
                dbc.Row([
                dcc.Graph(id="bar-graph")
            ], className='mb-3')
        ]),
        html.Div([
                dbc.Row([
                dcc.Dropdown(
                        id="histogram-dropdown",
                        options=data.columns,
                        multi=False,
                        value=default_axis
                    )
                ], className='mb-3'),
               

                dbc.Row([
                dbc.Button('Update Histogram & Box Whisker', id='button-2', n_clicks=0, style={"width": "100%"})
                ],className='mb-3'),
                dbc.Row([
                dcc.Graph(id="histogram")
            ], className='mb-3')
        ]),
        html.Div([
                dbc.Row([
                dcc.Graph(id="box-whisker")
            ], className='mb-3')
        ]),
        html.Div([
                dbc.Row([
                dcc.Dropdown(
                        id="scatter-plot-dropdown",
                        options=data.columns,
                        multi=True,

                    )
                ], className='mb-3'),
                dbc.Row([
                html.H5("Scatter Matrix Plot of Correlations"),
                dcc.Graph(id="scatter-matrix")
            ], className='mb-3')
        ]),
        html.Div([
            dbc.Row([
                html.H5("Heatmap Correlation"),
                html.Img(src=dash.get_asset_url('scatter_matrix_heatmap.png'), style={"width": "100%", "height": "auto"}),
            ], className='mb-3')
        ])

    ])
])
@callback(
    Output("histogram", "figure"),
    Output("box-whisker", "figure"),
    Input('button-2', 'n_clicks'),
    State("histogram-dropdown", "value"),
)
def update_histogram(clicks,x_axis):
    fig = px.histogram(
        data,
        x=x_axis,
        nbins=30,  # Number of bins
        title="Distribution"
    )
    fig.update_traces(texttemplate='%{y}', textposition='auto')



    # Customize the appearance
    fig.update_layout(
        template="plotly_dark",  # Dark theme
        yaxis_title="Frequency",
        title=dict(x=0.5),  # Center the title
        font=dict(size=12),
        legend_title="Legend",
    )
    boxplot = px.box(data,x=x_axis,
                     title="Box Plot",
                     points="all")
    boxplot.update_layout(template='plotly_dark')


    return fig, boxplot

@callback(
    Output("bar-graph", "figure"),
    Input('my-button','n_clicks'),
    State("x-dropdown", "value"),
    State("y-dropdown", "value")
)

def update_bar_graph(clicks,x_dropdown, y_dropdown):
    bar_graph = px.bar(
        data,
        x=x_dropdown,
        y=y_dropdown,
        color=x_dropdown,
        color_continuous_scale="Blues",  # Reverse Blues color scale
        title="Bar Chart with Color Scale",
        category_orders={x_dropdown: data.sort_values(y_dropdown, ascending=False)[x_dropdown].tolist()}
        # Sort in descending order
    )
    # Update layout
    bar_graph.update_layout(
        template="plotly_dark",  # Dark theme
        xaxis_title=x_dropdown,
        yaxis_title=y_dropdown,
        # coloraxis_colorbar=dict(
        #     title="salary",
        #     tickvals=np.linspace(data[x_dropdown].min(), data[x_dropdown].max(),num=3),
        #     ticktext=["low", "medium", "high"]
        # )
    )

    return bar_graph

@callback(
    Output("scatter-matrix", "figure"),
    Input('scatter-plot-dropdown', 'value')
)
def update_scatter_matrix(option):
    scatter_matrix_fig = px.scatter_matrix(
        numeric_data,
        dimensions=option,
        title="Scatter Matrix Plot of Correlations",
        labels={col: col for col in numeric_data.columns}  # Update labels to columns
    )
    scatter_matrix_fig.update_traces(diagonal_visible=False, marker=dict(size=5,
                                                          opacity=0.6))  # hides diagonals, You can also set color to a column name if you want the colors to vary by a category in the data.
    scatter_matrix_fig.update_layout(
        template="plotly_dark",  # Dark theme
        dragmode='select',
        width=1500,
        height=1500
    )
    return scatter_matrix_fig



