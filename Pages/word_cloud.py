from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.express as px
from PIL import Image
import numpy as np
import pandas as pd
import os


data = pd.read_csv("../Data/cleaned_data.csv", index_col=0)
data = data.reset_index()

# Combine all job titles into a single string
text = " ".join(data['Job Title'].astype(str))

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color="black", colormap="viridis").generate(text)

# Convert the word cloud to an image
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout()

# Save the word cloud image to the specified directory
output_path = os.path.join("../assets", "wordcloud_job_titles.png")
wordcloud.to_file(output_path)

# Display the image in a Plotly environment (optional)
image = np.array(Image.open("wordcloud.png"))
fig = px.imshow(image, title="Word Cloud Visualization")
fig.update_layout(coloraxis_showscale=False)  # Remove color scale
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.show()
