
import pandas as pd
import plotly.express as px
import time
import os

data = pd.read_csv("../Data/cleaned_data.csv",index_col=0)


# Step 1: Calculate Total Observations for each Industry
filtered_data = data[data['Industry'] != 'Unknown']
total_observations = filtered_data.groupby("Industry").size()

# Step 2: Calculate Average Rating for each Industry
average_rating = filtered_data.groupby("Industry")["Rating"].mean()

# Step 3: Extract Industry Names
industry_names = total_observations.index  # This gives the unique industry names

# Step 4: Combine results into a new DataFrame
result = pd.DataFrame({
    "Industry": industry_names,
    "Total Observations": total_observations.values,
    "Average Rating": average_rating.values
})
print(result)
print(result.nlargest(10, "Total Observations"))# top 10 rated industries, filtered by industries with the highest total observations

# Step 5: Filter industries with the highest total observations
top_observations = result.nlargest(10, "Total Observations")

# Step 6: Sort by Average Rating within the filtered industries
top_rated_industries = top_observations.sort_values(by="Average Rating", ascending=True)

def update_bar_chart(x_axis,y_axis,top_bottom):
    fig = px.bar(
        top_rated_industries,
        x=x_axis,
        y=y_axis,
        color=x_axis,
        orientation='h',  # Horizontal bars
        color_continuous_scale='Viridis_r', #Blues_r
        range_color=(top_rated_industries[x_axis].min(), top_rated_industries[x_axis].max()),  # scale
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
            tickvals=[top_rated_industries[x_axis].min(), top_rated_industries[x_axis].max()],
            ticktext=['0', '5']
        ),
        template="plotly_dark"  # Dark theme
    )

    # # Generate a timestamped filename
    # timestamp = time.strftime("%Y%m%d-%H%M%S")  # Format: YYYYMMDD-HHMMSS
    # filename = os.path.join(save_directory, f"bar_chart_{timestamp}.png")
    #
    # # Save the figure as an image
    # fig.write_image(filename)
    fig.show()

    return "return in ide"

update_bar_chart('Average Rating','Industry','Top')