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
    html.H1("Insights"),
    ],className='mb-3'),

    dbc.Row([
        dbc.Col([
            html.H2("Rating Analysis"),
            html.H4("Which industries have the highest and lowest average ratings?"),
            html.Img(src=dash.get_asset_url('top_10_sectors_by_rating.png'),
                                 style={"width": "100%", "height": "auto"}),
            html.Img(src=dash.get_asset_url('bottom_10_sectors_by_rating.png'),
                                 style={"width": "100%", "height": "auto"}),
            html.H4("Do smaller companies (in size or revenue) tend to have lower ratings?"),
            html.H4("Are low-rated companies offering lower salaries than high-rated ones?"),
            html.H4("Analyze trends in ratings over time"),
            html.H4("Analyze correlations between Rating and numeric variables like Min Salary or Max Salary"),
            html.H4("Are low-rated companies offering lower salaries than high-rated ones?"),
            html.H4("Are low-rated companies offering lower salaries than high-rated ones?")

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
