import pandas as pd

# Load CSV into a pandas DataFrame
df = pd.read_csv('job_list.csv')

# Convert DataFrame to HTML
html_table = df.to_html(index=False)

# Save the HTML to a file
with open("output.html", "w", encoding="utf-8") as file:
    file.write(html_table)

