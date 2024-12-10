
import pandas as pd
import plotly.express as px
import time
import os
import pandas as pd
from collections import Counter
import re
from nltk.corpus import stopwords

data = pd.read_csv("../Data/cleaned_data.csv",index_col=0)
data = data.reset_index()

#Technical Skills
data['python_job'] = data['Job Description'].str.contains('python')
data['SQL_job'] = data['Job Description'].str.contains('sql')
data['Tableau_job'] = data['Job Description'].str.contains('tableau')
data['excel_job'] = data['Job Description'].str.contains('excel')
data['PowerBI_job'] = data['Job Description'].str.contains('powerbi')
data['Matplotlib_job'] = data['Job Description'].str.contains('matplotlib')
data['Looker_job'] = data['Job Description'].str.contains('looker')
data['ai_job'] = data['Job Description'].str.contains('ai')
data['machine_learning_job'] = data['Job Description'].str.contains('machine learning')
# print("Python:"+str(data['python_job'].value_counts()))
# print(data['SQL_job'].value_counts())
# print(data['Tableau_job'].value_counts())
# print(data['excel_job'].value_counts())
# print(data['ai_job'].value_counts())
# print(data['machine_learning_job'].value_counts())

#Soft Skills
data['Communication_skill'] = data['Job Description'].str.contains('communication')
data['Critical_Thinking_skill'] = data['Job Description'].str.contains('critical thinking')
data['Problem_Solving_skill'] = data['Job Description'].str.contains('problem solving')
# print(data['Communication_skill'].value_counts())
# print(data['Critical_Thinking_skill'].value_counts())
# print(f"Problem Solving Skills : {data['Problem_Solving_skill'].value_counts()} ")

# Print the most common words
# Load NLTK's stop words
# import nltk
# nltk.download('stopwords')
# stop_words = set(stopwords.words('english'))
# # Combine all job descriptions into a single string
# all_descriptions = " ".join(data['Job Description'].astype(str))
#
# # Clean the text: Remove punctuation, numbers, and convert to lowercase
# cleaned_text = re.sub(r'[^a-zA-Z\s]', '', all_descriptions).lower()
#
# # Tokenize the text into words
# words = cleaned_text.split()
#
# # Remove stop words
# filtered_words = [word for word in words if word not in stop_words]
#
# # Count the frequency of each word
# word_counts = Counter(filtered_words)
#
# # Get the 10 most common words
# common_words = word_counts.most_common(20)
# # Convert to DataFrame for display
# common_words_df = pd.DataFrame(common_words, columns=["Word", "Frequency"])
# # print(common_words_df)

technical_skills_df = data[['Job Title','python_job', 'SQL_job','excel_job','Tableau_job','PowerBI_job','Matplotlib_job','Looker_job','ai_job','machine_learning_job']].copy()


# List of Top Data Analyst roles based on observations
roles =  ["Data Analyst",
    "Senior Data Analyst",
    "Junior Data Analyst",
    "Business Data Analyst",
    "Data Analyst II",
    "Data Quality Analyst",
    "Data Governance Analyst",
    "Lead Data Analyst",
    "Data Reporting Analyst",
    "Financial Data Analyst",
          ]


data = data[data["Job Title"].isin(roles)]

df4 = data[['Job Title','python_job', 'SQL_job','excel_job','Tableau_job']].copy()

Lang = df4.groupby('Job Title')[['python_job', 'SQL_job','excel_job','Tableau_job']].sum().sort_values(by='python_job',ascending=False).head(10)
df_lang = pd.DataFrame(Lang)
df_lang = df_lang.reset_index()

df_lang['number_of_job_openings'] = data['Job Title'].value_counts()[:10].values
columnsTitles = ['Job Title', 'number_of_job_openings','python_job', 'SQL_job','excel_job','Tableau_job']

df_lang = df_lang.reindex(columns=columnsTitles)

df_lang
fig = px.bar(df_lang, x='Job Title', y=['python_job', 'SQL_job','excel_job','Tableau_job'], title="Languages")
fig.show()
# def update_bar_chart(x_axis):
#     fig = px.bar(
#         df_lang,
#         x=x_axis,
#         y=['python_job', 'SQL_job'],
#         color=['python_job', 'SQL_job'],
#         orientation='v',  # Horizontal bars
#         # color_continuous_scale='Viridis_r',
#         color_continuous_scale='Blues',
#         # range_color=(top_rated_role[y_axis].min(), top_rated_role[y_axis].max()),  # scale
#         # title= f"{top_bottom} 10 {y_axis} by {x_axis}"
#         title = 'Top 10 Rated Roles'
#     )
#
#     # Customize layout
#     fig.update_layout(
#         height=600,
#         title_font_size=20,
#         # xaxis_title= f"{x_axis}",
#         xaxis_title = 'Roles',
#         # yaxis_title= f"{y_axis}",
#         coloraxis_colorbar=dict(
#             title= f"Rating Scale",
#             # tickvals=[top_rated_role[y_axis].min(), top_rated_role[y_axis].max()],
#             ticktext=['0', '5']
#         ),
#         template="plotly_dark"  # Dark theme
#     )
#
#     # # Generate a timestamped filename
#     # timestamp = time.strftime("%Y%m%d-%H%M%S")  # Format: YYYYMMDD-HHMMSS
#     # filename = os.path.join(save_directory, f"bar_chart_{timestamp}.png")
#     #
#     # # Save the figure as an image
#     # fig.write_image(filename)
#     # fig.write_image(os.path.join("../assets", "top_10_rated_roles.png"))
#     fig.show()
#
#     return "return in ide"
#
# update_bar_chart('Job Title')