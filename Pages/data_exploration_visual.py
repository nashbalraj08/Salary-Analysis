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
        ]),

            dbc.Row([
            html.H1("Distribution Analysis"),
            ],className='mb-3'),
            dbc.Row([
                html.H5("Distribution of Rating"),
            ], className='mb-3'),
            dbc.Row([
                dbc.Col([
                    html.Img(src=dash.get_asset_url('Distribution of Rating.png'),
                             style={"width": "100%", "height": "auto"})],
                    width=6),
                dbc.Col([
                    dcc.Markdown('''
         ## Insights
         * Ratings are positively skewed, with a majority of ratings clustering between 3.5 and 4.5
         * There are fewer ratings below 2.5, indicating most companies are rated relatively high
         * Slight Left Skew: The slight left skew in the distribution indicates that there are 
         some lower outliers, a few companies have ratings below 1, which are potential outliers or reflect poorly-rated companies

         ## Questions to Explore:
         1. Which industries have the highest and lowest average ratings?
         2. Do smaller companies (in size or revenue) tend to have lower ratings?
         3. Are low-rated companies offering lower salaries than high-rated ones?
         4. Analyze trends in ratings over time (if the Founded column indicates company age)
         5. Analyze correlations between Rating and numeric variables like Min Salary or Max Salary
         6. Explore their job descriptions and industries to find patterns
         7. Look at additional factors like company size or ownership type to understand challenges.
         8. Compare Ratings by Categories 
             * Industry: Are certain industries consistently rated higher or lower?
             * Company Size: Do larger companies have higher ratings compared to smaller ones?
             * Revenue: Explore if company revenue correlates with better ratings.

         '''

                                 )

                ], width=6),

            ], className='mb-3'),


                dbc.Row([
                    html.H5("Distribution of Founded")
                ], className='mb-3'),
                dbc.Row([
                    dbc.Col([
                        html.Img(src=dash.get_asset_url('Distribution of Founded.png'),
                                 style={"width": "100%", "height": "auto"})],
                        width=6),
                    dbc.Col([
                        dcc.Markdown('''
                       ## Insights
                     * The histogram shows that most companies were founded after 1950, with a large spike after 2000 (660 companies).
                     * Older Companies: A small number of companies were founded before 1900, appearing as outliers in the data.
                     * Slight Left Skew: The slight left skew in the distribution indicates that there are some lower outliers, a few companies have ratings below 1, which are potential outliers or reflect poorly-rated companies.
                     * The boxplot confirms the presence of significant outliers, particularly companies founded before 1850.
                     * The IQR shows most of the data falls between 1970 and 2006, indicating the bulk of companies are relatively modern.
                     * The lower whisker represents the minimum year founded in 1682, excluding outliers, indicating that most companies are founded after 1916.
                     * Q1 --> This means that 25% of companies were founded in 1970 or below.
                     * Median --> The vertical line inside the box plot represents the median, meaning that half of the companies founded are in 1997 or below, while the other half founded after 1997.
                     * Q3 --> This indicates that 75% companies were founded in 2006 or below, while the top 25% founded after 2006
                     * The upper whisker represents the maximum year founded in 2019 in the data, excluding outlier
        
                     ## Questions to Explore:
                     1. Which industries have the highest and lowest average ratings?
                     2. Do smaller companies (in size or revenue) tend to have lower ratings?
                     3. Are low-rated companies offering lower salaries than high-rated ones?
                     4. Analyze trends in ratings over time (if the Founded column indicates company age).
                     5. Analyze correlations between Rating and numeric variables like Min Salary or Max Salary.
                     6. Explore their job descriptions and industries to find patterns.
                     7. Look at additional factors like company size or ownership type to understand challenges.
                     8. Compare Ratings by Categories 
                         * Industry: Are certain industries consistently rated higher or lower?
                         * Company Size: Do larger companies have higher ratings compared to smaller ones?
                         * Revenue: Explore if company revenue correlates with better ratings.
        
                      '''

                                     )

                    ], width=6),

                ], className='mb-3'),

                dbc.Row([

                    dbc.Col([
                        html.H5("Distribution of Minimum Salary"),
                        html.Img(src=dash.get_asset_url('Distribution of Minimum Salary.png'),
                                 style={"width": "100%", "height": "auto"})
                    ], width=6),
                    dbc.Col([
                        dcc.Markdown('''
                      ## Insights
                     * The histogram shows most salaries fall between 40k and 60k, with the peak at 40k (366 observations).
                     * Some salaries are below 30k, representing potential outliers or lower-paying roles.
                     * Right Skew: The histogram shows a slight right skew, with fewer observations above 70k, indicating the mean is higher than the median
                     * The boxplot confirms the presence of significant outliers  on the higher ends.
                     * The (IQR) lies between 40k and 60k, indicating this is where most of the salaries cluster.
                     * The lower whisker represents the minimum salary 24k, excluding outliers, indicating that most salaries are above 24k.
                     * Q1 --> This means that 25% of salaries are 41k or below.
                     * Median --> The vertical line inside the box plot represents the median, meaning that half of the salaries are 50k or below, while the other half above 50k.
                     * Q3 --> This indicates that 75% of salaries are 64k or below, while the top 25% above 64k
                     * The upper whisker represents the maximum salary,11.3k in the minimum salary range in the data, excluding outlier
        
                        Given this distribution, most salaries are clustered between $41k(Q1) and $64k(Q3). 
                        The mean is approximately $54260.98, and the median is $51k. Also, the standard deviation $19573.023k
                        This means most salaries tend to be within (+ —) $19573.023k of the mean. 
                        Therefore, acceptable prediction errors larger than $25k is not ideal, as this is higher than IQR (Q3-Q1) $23k represent a considerable gap.
                        Therefore, $19K of prediction error is acceptable, since within the standard deviation, which represents the typical spread of data and
                        below the IQR which captures a significant portion of the data without being too lenient.
        
                     ## Questions to Explore:
                     1. Industry: Do certain industries consistently offer higher minimum salaries?
                     2. Location: Are higher salaries concentrated in specific cities or regions?
                     3. Company Size: Larger companies might offer higher minimum salaries.
                     4. Assess relationships between Min Salary and other variables such as Rating or Max Salary
                     5. Explore trends in salaries over time (e.g., do newer companies offer higher starting salaries?
                     6. Compare Min Salary with Max Salary to identify salary ranges and gaps for specific roles or industries
                     7. What locations or company characteristics are associated with salaries above 70k?
                     8. Should roles with lower minimum salaries be flagged for potential investigation?
                    ''')
                    ], width=6)
                ], className='mb-3'),
                dbc.Row([

                        dbc.Col([
                            html.H5("Distribution of Maximum Salary"),
                            html.Img(src=dash.get_asset_url('Distribution of Maximum Salary.png'),
                                     style={"width": "100%", "height": "auto"}),
                            html.Img(src=dash.get_asset_url('Basic Stats Maximum Salary.png'),
                                     style={"width": "100%", "height": "auto"})
                        ], width=6),
                        dbc.Col([
                            dcc.Markdown('''
                          ## Insights
                         * The histogram shows most maximum salaries cluster between $60k and $100k, with a peak at $80k (381 observations).
                         * Significant outliers exist above $160k, particularly at $180k and $200k.
                         * Slightly Right Skew: The histogram shows a slight right skew, with fewer observations above $120k, indicating the mean is higher than the median
                         * The boxplot confirms the presence of significant outliers  on the higher ends.
                         * The (IQR) lies between $80k and $120k, indicating this is where most of the salaries cluster.
                         * The lower whisker represents the minimum salary 38k, excluding outliers, indicating that most salaries are above 38k.
                         * Q1 --> This means that 25% of salaries are 70k or below.
                         * Median --> The vertical line inside the box plot represents the median, meaning that half of the salaries are 87k or below, while the other half above
                         * Q3 --> This indicates that 75% of salaries are 104k or below, while the top 25% are above
                         * The upper whisker represents the maximum salary,151k in the maximum salary range in the data,excluding outliers
                
                            Given this distribution, most salaries are clustered between $70k(Q1) and $107k(Q3). 
                            The mean is approximately $89973.81k, and the median is $87k. Also, the standard deviation means most salaries tend to be within (+ —) $29310.18k of the mean. 
                            Therefore, acceptable prediction errors larger than $40k is not ideal, as this is higher than IQR (Q3-Q1) $37k which will represent a considerable gap.
                            Therefore, $29K of prediction error is acceptable, since within the standard deviation, which represents the typical spread of data and
                            below the IQR which captures a significant portion of the data without being too lenient.
                
                         ## Questions to Explore:
                         1. Salaries exceeding $140k or below $60k should be examined:Are they tied to specific industries or job titles?Do they represent niche roles, executive positions, or potential data errors?
                         2. Industry: Do high-salary roles cluster in specific sectors like technology or finance?
                         3. Location: Are certain cities or regions associated with higher maximum salaries?
                         4. Company Size: Larger companies may offer higher salary ceilings.
                         5. Test if higher maximum salaries correlate with company ratings.
                         6. Compare Min Salary with Max Salary to identify salary ranges and gaps for specific roles or industries
                         7. Are certain regions more likely to offer salaries in the $150k+ range?
                        ''')
                        ], width=6)
                    ], className='mb-3'),

                dbc.Row([
                    dbc.Col([
                        html.H5("Correlation Analysis of Numeric Variables"),
                        html.Img(src=dash.get_asset_url('scatter_matrix_heatmap.png'),
                                 style={"width": "100%", "height": "auto"}),
                        html.Img(src=dash.get_asset_url('scatter_matrix_heatmap_adjusted.png'),
                                 style={"width": "100%", "height": "auto"})
                    ], width=6),
                    dbc.Col([dcc.Markdown('''
                ## Insights
                * High correlation (0.86): Indicates that Min Salary and Max Salary are strongly related. This suggests they 
                    contain redundant information since we split it from variable of Salary ranges 
                * Create new variables that might provide better insights such as 
                    * Salary Range = Max Salary - Min Salary
                    * Salary Midpoint = (Max Salary + Min Salary) / 2
                * Second scatter matrix shows :
                    * Salary Range has a moderate positive correlation (0.78) with Max Salary and a weaker correlation (0.35) 
                        with Min Salary. This makes sense because the range is more influenced by the variability in 
                        maximum salaries.
                    * Salary Midpoint is strongly correlated with both Min Salary (0.95) and Max Salary (0.98). This is expected, 
                        as it is derived from their averages.
        
        
                ''')], width=6)
                ], className='mb-3'),
                dbc.Row([
        dbc.Col([
            html.H5("Correlation Analysis of Categorical Variables "),
            html.Img(src=dash.get_asset_url('heatmap_20241204-145249.png'), style={"width": "100%", "height": "auto"}),
            html.Img(src=dash.get_asset_url('heatmap_20241204-145252.png'), style={"width": "100%", "height": "auto"}),
            html.Img(src=dash.get_asset_url('heatmap_20241204-145339.png'), style={"width": "100%", "height": "auto"})
        ], width=6),
        dbc.Col([dcc.Markdown('''
        ## Insights
        * remove sector government as its highly correlated with government 


        ''')], width=6)
    ], className='mb-3'),
                dbc.Row([
        dbc.Col([
            html.H5("Correlation Analysis of Numeric & Categorical Variables "),
            html.Img(src=dash.get_asset_url('heatmap_20241204-145536.png'), style={"width": "100%", "height": "auto"})
        ], width=6),
        dbc.Col([dcc.Markdown('''
        No highly correlated variables for categorical variables.
        Highly correlated variables for certain numeric variables but is acceptable

        ''')], width=6)
    ], className='mb-3'),
                dbc.Row([
                    dbc.Col([
                        html.H5("Categorical Variable Analysis"),
                        html.Img(src=dash.get_asset_url('Top 10_Most_Common_Industries.png'),
                                 style={"width": "100%", "height": "auto"}),
                        html.Img(src=dash.get_asset_url('Top_10_Most_Common_Company_Names.png'),
                                 style={"width": "100%", "height": "auto"}),
                        html.Img(src=dash.get_asset_url('Top_10_Most_Common_Headquarters.png'),
                                 style={"width": "100%", "height": "auto"}),
                        html.Img(src=dash.get_asset_url('Top_10_Most_Common_Location.png'),
                                 style={"width": "100%", "height": "auto"}),
                        html.Img(src=dash.get_asset_url('Top_10_Most_Common_Sectors.png'),
                                 style={"width": "100%", "height": "auto"}),

                    ], width=6),
                    dbc.Col([dcc.Markdown('''
                ## Insights
        
                ## Questions to Explore:
        
                ''')], width=6)
                ], className='mb-3'),
                dbc.Row([
                    dbc.Col([
                        html.H5("Categorical Variable Analysis"),
                        html.Img(src=dash.get_asset_url('Top 10_Most_Common_Industries.png'),
                                 style={"width": "100%", "height": "auto"}),
                        html.Img(src=dash.get_asset_url('Top_10_Most_Common_Company_Names.png'),
                                 style={"width": "100%", "height": "auto"}),
                        html.Img(src=dash.get_asset_url('Top_10_Most_Common_Headquarters.png'),
                                 style={"width": "100%", "height": "auto"}),
                        html.Img(src=dash.get_asset_url('Top_10_Most_Common_Location.png'),
                                 style={"width": "100%", "height": "auto"}),
                        html.Img(src=dash.get_asset_url('Top_10_Most_Common_Sectors.png'),
                                 style={"width": "100%", "height": "auto"}),

                    ], width=6),
                    dbc.Col([dcc.Markdown('''
                ## Insights
        
                ## Questions to Explore:
        
                ''')], width=6)
                ], className='mb-3'),
                dbc.Row([
                    dbc.Col([
                        html.H5("Salary Analysis")
                    ], width=6),
                    dbc.Col([dcc.Markdown('''
                Analyze Min Salary and Max Salary distribution.
                Compare salaries by Industry or Location using boxplots.
                ## Insights
                   top 10 companies with the most "Easy Apply" job postings
                    df_easy_apply = cleaned_df[cleaned_df['Easy Apply'] == True] #Filters the data DataFrame to include only rows where 'Easy Apply' is True.
        
                    top_companies = cleaned_df[cleaned_df['Easy Apply']].groupby('Company Name').size().nlargest(10)
        
                    print("Top 10 companies with the most 'Easy Apply' job postings:")
                    print(top_companies)
        
                ## Questions to Explore: is as follows
        
                ''')], width=6)
                ], className='mb-3')



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
        color='Rating',
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



