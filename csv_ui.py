import pandas as pd
from datetime import datetime

# === Configuration ===
csv_file = "job_list.csv"
html_file = "index.html"
columns_to_include = ['Company', 'Title', 'Location', 'Created-TimeStamp']

# === Load and filter CSV ===
df = pd.read_csv(csv_file)

# === Keep only specific columns ===
df = df[columns_to_include]

# === Format date columns to 'YY-MM-DD' ===
date_columns = ['Created-TimeStamp']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%d-%m-%Y')

# === Convert to HTML table ===
html_table = df.to_html(index=False, classes="display", table_id="jobTable")

# === Full HTML with DataTables + Filters ===
html_output = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Filtered Job Listings</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
    <script src="https://code.jquery.com/jquery-3.7.0.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    <script>
    $(document).ready(function() {{
        $('#jobTable').DataTable({{
            "pageLength": 25,
            initComplete: function () {{
                this.api().columns().every(function () {{
                    var column = this;
                    var select = $('<select><option value=""></option></select>')
                        .appendTo($(column.footer()).empty())
                        .on('change', function () {{
                            var val = $.fn.dataTable.util.escapeRegex($(this).val());
                            column.search(val ? '^'+val+'$' : '', true, false).draw();
                        }});
                    column.data().unique().sort().each(function (d) {{
                        if (d) select.append('<option value="'+d+'">'+d+'</option>')
                    }});
                }});
            }}
        }});
    }});
    </script>
    <style>
        table.dataTable tfoot th {{
            padding: 5px;
        }}
        tfoot {{
            display: table-header-group;
        }}
    </style>
</head>
<body>
    <h2>Job Listings (Filtered)</h2>
    {html_table}
</body>
</html>
"""

# === Save HTML file ===
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"✅ Filtered HTML with selected columns and formatted dates saved to {html_file}")
