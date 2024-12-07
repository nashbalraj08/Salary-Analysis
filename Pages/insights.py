from dash import Dash, dcc, html, Input, Output, callback,Patch, State
import dash_bootstrap_components as dbc
import plotly.express as px
import dash
import dash_ag_grid as dag
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

dash.register_page(__name__, "/")


layout = dbc.Container([

    dbc.Row([
    dbc.Col([
        html.H2("Rating Analysis"),
        html.H4("Which industries have the highest and lowest average ratings?"),
        html.Img(src=dash.get_asset_url('top 10 industry by rating.png'),
                 style={"width": "100%", "height": "auto"}),
        html.Img(src=dash.get_asset_url('bottom 10 industry by rating.png'),
                 style={"width": "100%", "height": "auto"}),
        html.Img(src=dash.get_asset_url('Top 10_Most_Common_Industries.png'),
                 style={"width": "100%", "height": "auto"}),
    ], width=6),
    dbc.Col([dcc.Markdown('''
                     ## Insights
                     * Top rated industry is Audiovisual 
                        * the reason for this industry being the most highly rated is because there 
                          is only one observation the whole dataset with rating score of 5
                     * The second highly rated industry is Architectural & Engineering Services, 
                        with 8 observations, and average rating of 4.26
                     * The third top rated industry is Colleges & Universities,with only have 39 
                        observations and average rating of 4.16
                     * Since, the top 3 rated industries have low observations and not part of 
                        the top 10 most common industries in teh dataset. There should be ignored
                        since provide false information that new data analyst will seek in applying
                        for jobs since their look highly rated but not enough information from users
                        suggest their are popular industries       
                     * Bottom rated industries is only have one observation therefore not meaningful
    
    ''')], width=6),
    ],className='mb-3'),



    dbc.Row([
        dbc.Col([
            html.H2("Rating Analysis"),
            html.H4("Which industries have the highest and lowest average ratings?"),
            html.Img(src=dash.get_asset_url('top 10 industry by rating.png'),
                                 style={"width": "100%", "height": "auto"}),
            html.Img(src=dash.get_asset_url('bottom 10 industry by rating.png'),
                                 style={"width": "100%", "height": "auto"}),
            html.H4("Do smaller companies (in size or revenue) tend to have lower ratings?"),
            html.Img(src=dash.get_asset_url('company size by rating.png'),
                                 style={"width": "100%", "height": "auto"}),
            html.H4("Are low-rated companies offering lower salaries than high-rated ones?"),
            html.Img(src=dash.get_asset_url('company size by salary range.png'),
                                 style={"width": "100%", "height": "auto"}),
            html.H4("Analyze trends in ratings over time"),
            html.Img(src=dash.get_asset_url('rating over time.png'),
                                 style={"width": "100%", "height": "auto"}),
            html.H4("Analyze correlations between Rating and numeric variables like Min Salary or Max Salary"),
            html.Img(src=dash.get_asset_url('scatter_matrix_heatmap_adjusted.png'),
                                 style={"width": "100%", "height": "auto"})


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
