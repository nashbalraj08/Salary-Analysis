
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
# print(result)


def top_bottom_10(df, groupby_var, measurement_var, top_bottom=10, order="Top"):
    # Group by the specified variable and calculate the average of the measurement variable
    grouped_avg = df.groupby(groupby_var)['Total Observations'].mean().sort_values(ascending=True)
    # Select top or bottom N groups
    if order == "Top":
        result = grouped_avg.tail(top_bottom)
    elif order == "Bottom":
        result = grouped_avg.head(top_bottom)
    else:
        raise ValueError("The 'order' parameter must be 'top' or 'bottom'.")

    # Convert the result into a DataFrame and reset the index
    result_df = result.reset_index()
    # print(result_df)

    return result_df

# top_bottom_10(result, 'Industry', 'Average Rating', 10, "Top")

def update_bar_chart(x_axis,y_axis,top_bottom):
    x_axis='Average Rating'
    # Create bar chart with Plotly Express
    bottom_top = top_bottom_10(result, y_axis, x_axis, 10, top_bottom)
    fig = px.bar(
        bottom_top,
        x=x_axis,
        y=y_axis,
        color=x_axis,
        orientation='h',  # Horizontal bars
        color_continuous_scale='Viridis_r', #Blues_r
        range_color=(bottom_top[x_axis].min(), bottom_top[x_axis].max()),  # scale
        title= f"{top_bottom} 10 Company {y_axis} by {x_axis}"
    )

    # Customize layout
    fig.update_layout(
        height=600,
        title_font_size=20,
        xaxis_title= f"{x_axis}",
        yaxis_title= f"{y_axis}",
        coloraxis_colorbar=dict(
            title= f"{x_axis}",
            tickvals=[bottom_top[x_axis].min(), bottom_top[x_axis].max()],
            ticktext=['Low', 'High']
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