This script:

    Normalizes country names.
    Sorts film titles by submission season (August–March grouping).
    Adjusts the color scale so that the USA and Germany do not skew the visualization.
    Ensures actual film counts display on hover while keeping a proper color gradient.
    Formats film titles as "Movie Title (YEAR)".
    Implements a dynamic on-click feature to display film titles.

No additional files are needed beyond the CSV file containing the film submission data. As long as you have a CSV structured similarly to FilmFreeway-Submissions-2025-02-06-14-16-50.csv, the script will work.

However, to ensure it runs correctly, make sure:

    The CSV file contains at least these columns:
        "Project Title" (film name)
        "Country of Origin" (country names)
        "Submission Date" (dates formatted as YYYY-MM-DD or similar)

    You update file_path in the script to point to the actual location of your CSV file.

    You have Plotly and Pandas installed in your Python environment. If not, install them with:

pip install plotly pandas

The script writes an interactive HTML file (choropleth_map_final_corrected.html). You can open this in any web browser—no additional dependencies required.
