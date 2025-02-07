import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio

# Load the dataset
file_path = "/mnt/data/FilmFreeway-Submissions-2025-02-06-14-16-50.csv"
df = pd.read_csv(file_path)

# Convert submission date to datetime
df["Submission Date"] = pd.to_datetime(df["Submission Date"], errors="coerce")

# Function to determine the season year based on submission date
def get_season_year(date):
    if pd.isnull(date):
        return "Unknown"
    year = date.year
    month = date.month
    return year + 1 if month >= 8 else year

# Apply function to get the correct season year
df["Season Year"] = df["Submission Date"].apply(get_season_year)

# Sort films by season year, then alphabetically within each season
df_sorted = df.sort_values(by=["Season Year", "Project Title"])

# Format titles as "Movie Title (YEAR)"
df_sorted["Formatted Title"] = df_sorted.apply(lambda row: f"{row['Project Title']} ({row['Season Year']})", axis=1)

# Group by country and combine formatted titles into a properly sorted multiline string
choropleth_data_sorted = df_sorted.groupby("Normalized Country")["Formatted Title"].apply(lambda x: "<br>".join(x)).reset_index()
choropleth_data_sorted.rename(columns={"Formatted Title": "Formatted Titles"}, inplace=True)

# Ensure we only keep relevant columns before merging
choropleth_data = df.groupby("Normalized Country").size().reset_index(name="Film Count")

# Find the highest film count excluding the USA and Germany for color adjustment
top_countries = ["United States", "Germany"]
max_non_top_country = choropleth_data[~choropleth_data["Normalized Country"].isin(top_countries)]["Film Count"].max()

# Adjust color scale while keeping the real count for hover display
choropleth_data["Adjusted Film Count"] = np.where(
    choropleth_data["Normalized Country"].isin(top_countries), 
    max_non_top_country,  # Force USA and Germany to appear yellow without distorting the scale
    choropleth_data["Film Count"]
)

# Merge sorted film titles back into the dataset
choropleth_data = pd.merge(choropleth_data, choropleth_data_sorted, on="Normalized Country", how="left")

# Generate the choropleth map
fig = px.choropleth(
    choropleth_data,
    locations="Normalized Country",
    locationmode="country names",
    color="Adjusted Film Count",
    hover_name="Normalized Country",
    hover_data={"Film Count": True},
    title="Film Submissions by Country (Final with Chronological Sorting)",
    color_continuous_scale=px.colors.sequential.Plasma
)

# Ensure film count is correctly displayed on hover, and click event is properly formatted
fig.update_traces(
    customdata=choropleth_data["Formatted Titles"],
    hovertemplate="<b>%{hovertext}</b><br>Film Count: %{z}<br>(Click for titles)"
)

# JavaScript for dynamic title display on click
click_script = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    var myPlot = document.getElementsByClassName('plotly-graph-div')[0];

    myPlot.on('plotly_click', function(data) {
        var titles = data.points[0].customdata;
        var country = data.points[0].hovertext;
        var titleDiv = document.getElementById('title-box');
        titleDiv.innerHTML = '<h3>' + country + '</h3><p>' + (titles ? titles.replace(/<br>/g, '<br>') : 'No films available') + '</p>';
    });
});
</script>

<div id="title-box" style="position: fixed; bottom: 10px; right: 10px; width: 300px; max-height: 400px; overflow-y: auto; background: white; border: 1px solid black; padding: 10px;"></div>
"""

# Save the final interactive map
map_file_path = "/mnt/data/choropleth_map_final_corrected.html"
html_content = pio.to_html(fig, full_html=True, include_plotlyjs="cdn") + click_script

with open(map_file_path, "w") as f:
    f.write(html_content)

# Provide the final file path
map_file_path
