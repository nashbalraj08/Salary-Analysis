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
             ''')
