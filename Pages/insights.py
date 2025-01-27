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

    dbc.Row([html.H1("Insights")],className='mb-3'),
    dbc.Row([html.H3("Which industries dominate company concentrations before and after 2000?")],className='mb-3'),
    dbc.Row([dbc.Col([html.H4("Before 2000 Analysis")],width=6),dbc.Col([html.H4("After 2000 Analysis")],width=6)],className='mb-3'),
    dbc.Row([
            dbc.Col([

                html.Img(src=dash.get_asset_url('before2000industry.png'),
                         style={"width": "100%", "height": "auto"}),
                dcc.Markdown('''
                         * Before 2000:
                            * Top Industry: Staffing & Outsourcing 
                            * The focus is on traditional industries like staffing, IT, healthcare, and finance, 
                                which were well-established sectors.
                         ''')
            ],width=6),
            dbc.Col([

                html.Img(src=dash.get_asset_url('after2000Industry.png'),
                         style={"width": "100%", "height": "auto"}),

                dcc.Markdown('''
                        * After 2000: 
                            * Top Industry: IT Services (overtakes Staffing & Outsourcing)
                            * There is a noticeable shift towards tech-centric industries (e.g., Internet, Software),
                                reflecting the tech boom and digital transformation post-2000
                         ''')],width=6)
        ],className='mb-3'),


    dbc.Row([html.H3("Do the older companies have significantly different ratings compared to modern companies?")],className='mb-3'),
    dbc.Row([html.Img(src=dash.get_asset_url('Comparison of Company Ratings Before and After 2000.png'),
                     style={"width": "100%", "height": "auto"})],className='mb-3'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('''
                         Before 2000:
                         * The (IQR) lies between 3.3 and 3.9, indicating this is where most of the rating cluster.
                         * The lower whisker represents the minimum rating 2.4, excluding outliers, indicating that most rating are above 2.4.
                         * Q1 --> This means that 25% of company rating are 3.3 or below.
                         * Median --> The vertical line inside the box plot represents the median, meaning that half of the rating scores are 3.6 or below, while the other half above
                         * Q3 --> This indicates that 75% of rating score are 3.9 or below, while the top 25% are above
                         * The upper whisker represents the maximum rating score 4.8,excluding outliers
                         * The interquartile range (IQR) for before 2000 is narrower, indicating less variation in ratings among older companies
                         * Both periods have outlier --> There are a few very low ratings (below 2.4), indicating some poorly rated companies.
                         * Companies founded before 2000 have a slightly narrower range of ratings compared to those founded after 2000, 
                                indicating more consistency in older companies' ratings
                         * Older companies appear to have more consistent but slightly lower ratings, possibly due to traditional practices or 
                                less emphasis on factors measured by rating systems
                         ''')
        ], width=6),
        dbc.Col([
            dcc.Markdown('''
                         After 2000: 
                         * The (IQR) lies between 3.4 and 4.4, indicating this is where most of the rating cluster.
                         * The lower whisker represents the minimum rating 1.9, excluding outliers, indicating that most rating are above 1.9
                         * Q1 --> This means that 25% of company rating are 3.4 or below.
                         * Median --> The vertical line inside the box plot represents the median, meaning that half of the rating scores are 3.9 or below, while the other half above
                         * Q3 --> This indicates that 75% of rating score are 4.4 or below, while the top 25% are above
                         * The upper whisker represents the maximum rating score 5,excluding outlier 
                         * Companies founded after 2000 have a higher median rating compared to those founded before 2000
                         * suggests that modern companies might focus more on factors contributing to higher ratings, 
                                    such as employee satisfaction or customer feedback
                         * The IQR for after 2000 is wider, showing more variability in modern company ratings
                         * Both periods have outlier --> A few extremely low outliers, though the majority of ratings are clustered closer to the median
                         ''')], width=6)
    ], className='mb-3'),

dbc.Row([html.H3("Do the older companies have significantly different salary compared to modern companies?")],className='mb-3'),
    dbc.Row([html.Img(src=dash.get_asset_url('Comparison of Salary before and after 2000.png'),
                     style={"width": "100%", "height": "auto"})],className='mb-3'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('''
                         Before 2000:
                         * The (IQR) lies between $56K and $80K,indicating most salaries are concentrated between Q1 and Q3, 
                         as shown by the density of points in the boxplot
                         * The lower whisker(data within 1.5 times the IQR) represents the minimum salary,excluding outliers, indicating that 
                         most salary are above $33K
                         * Q1 --> This means that 25% of data analyst salary are $56K or below.
                         * Median --> The vertical line inside the box plot represents the median, meaning that half 
                         of the salary are $68K or below, while the other half above
                         * Q3 --> This indicates that 75% of salary are $80K or below, while the top 25% are above
                         * The upper whisker(data within 1.5 times the IQR) represents the maximum salary $113k,excluding outliers
                         * The interquartile range (IQR) before 2000 is slightly wider (bigger IQR range), indicating
                          slightly more variation in salary among older companies than newer companies
                         * Companies founded before 2000 have a slightly wider range of salary compared to those founded after 2000, 
                                indicating less consistency in older companies' salary range
                         * Outliers --> There are points with very high salary (above $113k), highlighting the presence 
                            of highly paid individuals 
                         * Older companies appear to have less consistent but slightly lower salary
                         ''')
        ], width=6),
        dbc.Col([
            dcc.Markdown('''
                         After 2000: 
                         * The (IQR) lies between $59K and $81K, indicating most salaries are concentrated between Q1 and Q3, 
                         as shown by the density of points in the boxplot
                         * The lower whisker(data within 1.5 times the IQR) represents the minimum salary,excluding outliers, indicating that 
                         most salary are above $33K, similar to period before 2000
                         * Q1 --> This means that 25% of data analyst salary are $59K or below.
                         * Median --> The vertical line inside the box plot represents the median, meaning that half 
                         of the salary are $70K or below, while the other half above
                         * Q3 --> This indicates that 75% of salary are $81K or below, while the top 25% are above
                         * The upper whisker(data within 1.5 times the IQR) represents the maximum salary $113k,excluding outliers
                         * The interquartile range (IQR) before 2000 is slightly narrower (smaller IQR range), indicating
                          slightly less variation in salary among newer companies salaries than older companies salaries
                         * Companies founded after 2000 have a  narrower range of salary compared to those founded before 2000, 
                                indicating more consistency in newer companies' salary range
                         * Outliers --> There are points with very high salary (above $113k), highlighting the presence 
                            of highly paid individuals 
                         * Newer companies appear to have more consistent but similar salary range than older companies for Data Analyst
                         ''')], width=6)
    ], className='mb-3'),







    dbc.Row([html.H3("Are there geographical patterns in the dominance of companies before and after 2000?")],className='mb-3'),
    dbc.Row([dbc.Col([html.H4("Before 2000 Analysis")],width=6),dbc.Col([html.H4("After 2000 Analysis")],width=6)],className='mb-3'),
    dbc.Row([
            dbc.Col([

                html.Img(src=dash.get_asset_url('choropleth_map_before_2000.png'),
                         style={"width": "100%", "height": "auto"}),
                dcc.Markdown('''
                         * Before 2000:
                            * States like California (CA), Texas (TX), and Illinois (IL) show a high concentration of 
                                companies, indicating these were historically dominant hubs for businesses
                            * 
                         ''')
            ],width=6),
            dbc.Col([

                html.Img(src=dash.get_asset_url('choropleth_map_after_2000.png'),
                         style={"width": "100%", "height": "auto"}),

                dcc.Markdown('''
                        * After 2000: 
                            * The dominance of California (CA) and Texas (TX) continues, but their share has grown 
                                further, highlighting these states' growing appeal for newer companies
                            * California's sustained dominance (both before and after 2000) aligns with its role as the
                                global hub for technology and innovation.    
                            * States like New York and Pennsylvania see a decline 
                         ''')],width=6)
        ],className='mb-3'),

    dbc.Row([html.H3("Which states do companies offer better salaries?")],className='mb-3'),
    dbc.Row([
            dbc.Col([

                html.Img(src=dash.get_asset_url('choropleth_map_before_2000_salary.png'),
                         style={"width": "100%", "height": "auto"}),
                dcc.Markdown('''
                         * Before 2000:
                            * States with lower ranges, such as Colorado (CO) and Arizona (AZ), suggest that these 
                                areas were less developed in terms of offering competitive salaries during this period.
                            * 
                         ''')
            ],width=6),
            dbc.Col([

                html.Img(src=dash.get_asset_url('choropleth_map_after_2000_salary.png'),
                         style={"width": "100%", "height": "auto"}),

                dcc.Markdown('''
                        * After 2000: 
                            * California (CA) continues to lead in salary ranges across both time periods, but Texas 
                                (TX), Washington (WA), and Colorado (CO) are rapidly catching up after 2000.
                         ''')],width=6)
        ],className='mb-3'),

    dbc.Row([html.H3("Which states do companies offer better salaries?")],className='mb-3'),
    dbc.Row([
            dbc.Col([

                html.Img(src=dash.get_asset_url('choropleth_map_industry_before_2000.png'),
                         style={"width": "100%", "height": "auto"}),
                dcc.Markdown('''
                         * Before 2000:
                            * Dominance is more diverse, with industries like Banks & Credit Unions, Investment Banking 
                            & Asset Management, and Health Care Services & Hospitals playing key roles.
                         ''')
            ],width=6),
            dbc.Col([

                html.Img(src=dash.get_asset_url('choropleth_map_industry_after_2000.png'),
                         style={"width": "100%", "height": "auto"}),

                dcc.Markdown('''
                        * After 2000: 
                            * Industry dominance becomes more consolidated, 
                                with tech-related industries like IT Services, Computer Hardware & Software, and Staffing & Outsourcing taking over in most states
                            * Financial industries such as Banks & Credit Unions and Investment Banking & Asset Management, which were dominant before 2000, are no longer as prominent after 2000.
                                This indicates a shift away from traditional finance hubs to tech-centric industries.    
                            *The Consulting industry remains stable, maintaining a consistent presence in states like Illinois and Massachusetts across both periods.    
                        ''')],width=6)
        ],className='mb-3'),
    dbc.Row([html.Img(src=dash.get_asset_url('treemap_before_after_2000.png'),
                      style={"width": "100%", "height": "auto"})], className='mb-3'),

    html.H2("Rating Analysis"),
    dbc.Row([html.H3("What are the top 10 rated Roles?")],
            className='mb-3'),
    dbc.Row([
        dbc.Col([
            html.Img(src=dash.get_asset_url('skewed job roles.png'),
                     style={"width": "100%", "height": "auto"})
        ], width=6),
        dbc.Col([dcc.Markdown('''
                     ## Insights
                     * Top rated role is AI insights 
                        * the reason for this role being the most highly rated is because there 
                          is only one observation the whole dataset with rating score of 5, similar for next 5 roles
                     * Since, the top 5 rated roles have low observations and not part of 
                        the top 10 most common roles in the dataset. There should be ignored
                        since provide false information that new data analyst will seek in applying
                        for jobs since their look highly rated roles but not enough information from users
                        suggest their are popular roles       
                     

    '''),
                 html.Img(src=dash.get_asset_url('Top_10_Most_Common_Roles.png'),
                          style={"width": "100%", "height": "auto"})
                 ], width=6),
    ], className='mb-3'),
    dbc.Row([html.Img(src=dash.get_asset_url('top_10_rated_roles.png'),
                      style={"width": "100%", "height": "auto"})], className='mb-3'),


    dbc.Row([html.H3("Do the older companies have significantly different ratings compared to modern companies?")],className='mb-3'),
    dbc.Row([html.Img(src=dash.get_asset_url('Comparison of Company Ratings Before and After 2000.png'),
                     style={"width": "100%", "height": "auto"})],className='mb-3'),

    dbc.Row([
    dbc.Col([
        html.H4("Which industries have the highest and lowest average ratings?"),
        html.Img(src=dash.get_asset_url('top 10 industry by rating.png'),
                 style={"width": "100%", "height": "auto"}),
        html.Img(src=dash.get_asset_url('bottom 10 industry by rating.png'),
                 style={"width": "100%", "height": "auto"})
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
    
    '''),
             html.Img(src=dash.get_asset_url('Top 10_Most_Common_Industries.png'),
                      style={"width": "100%", "height": "auto"})
             ], width=6),
    ],className='mb-3'),

    dbc.Row([
        dbc.Col([
        html.Img(src=dash.get_asset_url('Top 10 Industies by Rating (cleanup).png'),
                 style={"width": "100%", "height": "auto"})
        ],width=6),
        dbc.Col([dcc.Markdown('''
        ## Insights
        * After cleaning up the data ensuring we only look at Industries that have the most observations, to find out
            which industries is highly rated. 
        * As you can see IT services, has the highest rating (4.05) compared to other industries and
            with 325 observations
        * Even though, staffing & outsourcing has 323 observations, the second highest industry with observations
            the rating with 3.78, is only 5th highly rated industry
                 
        ''')],width=6)
    ],className='mb-3'),

    dbc.Row([
        dbc.Col([
            html.H4("Do smaller companies (in size) tend to have lower ratings?"),
            html.Img(src=dash.get_asset_url('company size by rating.png'),
                                 style={"width": "100%", "height": "auto"})
        ],width=6),
        dbc.Col([ dcc.Markdown('''
                     ## Insights
                     * As you can see in the bar graph, the smaller companies with 
                     1 to 200 employees actually have high rating 
                     ''')],width=6)
    ],className='mb-3'),

    dbc.Row([
        dbc.Col([
            html.H4("Are highly-rated companies offering high salaries?"),
            html.Img(src=dash.get_asset_url('Top 10 Company highly rated.png'),
                     style={"width": "100%", "height": "auto"}),
            html.Img(src=dash.get_asset_url('Top 10 Company by Salary Range.png'),
                     style={"width": "100%", "height": "auto"})
        ],width=6),
        dbc.Col([ dcc.Markdown('''
                     ## Insights
                     * The top 3 highly rated companies is :
                        Staffigo, Apple and Kforce
                     * The top 3 Highly Rated companies with highest salary is:
                        Apple, Robert Half and Diverse Lynx
                     * In regards to apply, is offering the highest salary(High correlation: Apple demonstrates both 
                     high ratings and high salaries), but the other top 2 highly rated
                        are offering on average highly rated salary(Low correlation: Staffigo Technical Services, LLC, 
                        is highly rated but offers relatively lower salaries.)
                     * Highly-rated companies do not always offer the highest salaries, since Staffigo Technical 
                        Services, LLC, while the top-rated company, does not offer a top-tier salary, indicating a 
                        weaker correlation overall
                     * This mixed trend suggests that other factors beyond ratings may influence salary ranges.   
                     ''')],width=6)
    ],className='mb-3'),

    dbc.Row([
        dbc.Col([
            html.H4("Analyze trends in ratings over time"),
            html.Img(src=dash.get_asset_url('rating over time.png'),
                     style={"width": "100%", "height": "auto"})
        ],width=6),
        dbc.Col([ dcc.Markdown('''
                     ## Insights
                     * Over time companies rating increase 
                     * Older companies (founded before 1900) show fluctuating ratings, but ratings stabilize and improve 
                        slightly for companies founded after 1950.
                     ''')],width=6)
    ],className='mb-3'),

    dbc.Row([
        dbc.Col([
            html.H4("Analyze correlations between Rating and numeric variables like Min Salary or Max Salary"),
            html.Img(src=dash.get_asset_url('scatter_matrix_heatmap_adjusted.png'),
                     style={"width": "100%", "height": "auto"})
        ],width=6),
        dbc.Col([ dcc.Markdown('''
                     ## Insights
                     * There is no significant relationship between high ratings and high salaries, as 
                            indicated by the near-zero correlation values.
                     * The analysis supports the earlier observation: highly-rated companies do not 
                        consistently offer high salaries.
                     * The correlation between rating and max salary is only 0.05, indicating a very weak relationship. 
                        Other factors may influence salary more significantly than company ratings
                     ''')],width=6)
    ],className='mb-3'),

    dbc.Row([html.H3("Compare salaries by Industry")],className='mb-3'),
    dbc.Row([dbc.Col([html.H4("Before 2000 Analysis")],width=6),dbc.Col([html.H4("After 2000 Analysis")],width=6)],className='mb-3'),
    dbc.Row([
            dbc.Col([
                html.Img(src=dash.get_asset_url('boxplot_salary_industry_before_2000.png'),
                         style={"width": "100%", "height": "auto"}),
                dcc.Markdown('''
                         * Before 2000:
                            * Industries like Health Care Services & Hospitals and Investment Banking & Asset Management
                             have highest median salaries.
                            * Salaries are more compressed with smaller interquartile ranges, narrower spreads,indicating 
                                consistent pay scales
                            * Outliers present 
                            * Traditional industries like Health Care and Finance (Banks & Credit Unions) dominate salaries.
                         ''')
            ],width=6),
            dbc.Col([

                html.Img(src=dash.get_asset_url('boxplot_salary_industry_after_2000.png'),
                         style={"width": "100%", "height": "auto"}),

                dcc.Markdown('''
                        * After 2000: 
                            * Internet and IT Services industries lead with the highest median salaries
                            * A wider spread in salaries is evident,signaling more variance between high and low salaries.
                            * Outliers present,More frequent outlier than before 2000 suggest some very high-paying roles 
                            emerged post-2000.
                            * Technology-oriented industries like Internet, IT Services, and Software & Network Solutions 
                            take the lead, reflecting the growth of the tech sector.
                            
                         ''')],width=6)
        ],className='mb-3')


])
