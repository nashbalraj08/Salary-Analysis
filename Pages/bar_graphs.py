
import pandas as pd
import plotly.express as px
import time
import os

data = pd.read_csv("../Data/cleaned_data.csv",index_col=0)

#Industry vs Rating
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
# print(result.nlargest(10, "Total Observations"))# top 10 rated industries, filtered by industries with the highest total observations

# Step 5: Filter industries with the highest total observations
top_observations = result.nlargest(10, "Total Observations")

# Step 6: Sort by Average Rating within the filtered industries
top_rated_industries = top_observations.sort_values(by="Average Rating", ascending=True)

#Company Name vs Rating
# Step 1: Calculate Total Observations for each Company
filtered_data = data[data['Company Name'] != 'Unknown']
total_observations = filtered_data.groupby("Company Name").size()

# Step 2: Calculate Average Rating for each Company Name
average_rating = filtered_data.groupby("Company Name")["Rating"].mean()

# Step 3: Extract Industry Names
company_names = total_observations.index  # This gives the unique Company Name

# Step 4: Combine results into a new DataFrame
result2 = pd.DataFrame({
    "Company Name": company_names,
    "Total Observations": total_observations.values,
    "Average Rating": average_rating.values
})
# print(result2)
# print(result2.nlargest(10, "Total Observations"))# top 10 rated industries, filtered by industries with the highest total observations
# print(result2.nsmallest(20, "Total Observations"))# top 10 rated industries, filtered by industries with the highest total observations

# Step 5: Filter industries with the highest total observations
top_observations = result2.nlargest(10, "Total Observations")

# Step 6: Sort by Average Rating within the filtered industries
top_rated_company = top_observations.sort_values(by="Average Rating", ascending=True)


#Company Name vs Salary
# Step 1: Calculate Total Observations for each Company
filtered_data = data[data['Company Name'] != 'Unknown']
total_observations = filtered_data.groupby("Company Name").size()

# Step 2: Calculate Average Salary Range for each Company Name
average_salary = filtered_data.groupby("Company Name")["Salary Range"].mean()

# Step 3: Extract Industry Names
company_names = total_observations.index  # This gives the unique Company Name

# Step 4: Combine results into a new DataFrame
result3 = pd.DataFrame({
    "Company Name": company_names,
    "Total Observations": total_observations.values,
    "Salary Range": average_salary.values
})
# print(result3)
# print(result3.nlargest(10, "Total Observations"))# top 10 rated industries, filtered by industries with the highest total observations

# Step 5: Filter industries with the highest total observations
top_observations = result3.nlargest(10, "Total Observations")

# Step 6: Sort by Salary Range within the filtered industries
top_rated_company = top_observations.sort_values(by="Salary Range", ascending=True)



#Concentration of Companies Post-2000 by Industry
# Step 1: Calculate Total Observations for each Company
# Filter companies founded after 2000
post_2000_df = data[data['Industry'] != 'Unknown']
post_2000_df = post_2000_df[post_2000_df['Founded'] >= 2000]

# # Step 2: Count companies in each industry
industry_counts = post_2000_df['Industry'].value_counts().head(10)
print(industry_counts)



# Step 3: Extract Industry Names
industry_names = industry_counts.index  # This gives the unique Company Name

# Step 4: Combine results into a new DataFrame
result3 = pd.DataFrame({
    "Industry Name": industry_names,
    "Total Observations": industry_counts.values,
})
print(result3)
# print(result3.nlargest(10, "Total Observations"))# top 10 rated industries, filtered by industries with the highest total observations
#
# # Step 5: Filter industries with the highest total observations
# top_observations = result3.nlargest(10, "Total Observations")

# Step 6: Sort by Salary Range within the filtered industries
result3 = result3.sort_values(by="Total Observations", ascending=True)





def update_bar_chart(x_axis,y_axis,top_bottom):
    fig = px.bar(
        result3,
        x=x_axis,
        y=y_axis,
        color=x_axis,
        orientation='h',  # Horizontal bars
        # color_continuous_scale='Viridis_r',
        color_continuous_scale='Blues',
        range_color=(result3[x_axis].min(), result3[x_axis].max()),  # scale
        # title= f"{top_bottom} 10 {y_axis} by {x_axis}"
        title = 'Concentration of Companies After 2000 by Industry'
    )

    # Customize layout
    fig.update_layout(
        height=600,
        title_font_size=20,
        # xaxis_title= f"{x_axis}",
        xaxis_title = 'Number of Companies',
        yaxis_title= f"{y_axis}",
        coloraxis_colorbar=dict(
            title= f"{x_axis}",
            tickvals=[result3[x_axis].min(), result3[x_axis].max()],
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
    # fig.show()

    return "return in ide"

update_bar_chart('Total Observations','Industry Name','Top')