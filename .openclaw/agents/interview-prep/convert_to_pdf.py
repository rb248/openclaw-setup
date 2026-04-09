#!/usr/bin/env python3
"""Convert Markdown to PDF using WeasyPrint"""

import markdown
from weasyprint import HTML, CSS
import sys

# Input and output files
input_file = "/home/rb/.openclaw/workspace-interview-prep/AWS-SageMaker-Complete-Guide.md"
output_file = "/home/rb/.openclaw/workspace-interview-prep/AWS-SageMaker-Complete-Guide.pdf"

# Read markdown file
with open(input_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert markdown to HTML
html_content = markdown.markdown(
    md_content,
    extensions=['tables', 'fenced_code', 'toc']
)

# Add basic styling
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4;
            margin: 2.5cm;
            @bottom-center {{
                content: counter(page);
            }}
        }}
        body {{
            font-family: Georgia, serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #1a5276;
            border-bottom: 2px solid #1a5276;
            padding-bottom: 10px;
            page-break-before: always;
        }}
        h1:first-of-type {{
            page-break-before: avoid;
        }}
        h2 {{
            color: #2874a6;
            margin-top: 25px;
        }}
        h3 {{
            color: #5499c7;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: Monaco, monospace;
            font-size: 9pt;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 3px solid #1a5276;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10pt;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #1a5276;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        blockquote {{
            border-left: 4px solid #1a5276;
            margin: 15px 0;
            padding: 10px 20px;
            background-color: #f9f9f9;
        }}
        ul, ol {{
            margin: 10px 0;
            padding-left: 25px;
        }}
        li {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""

# Generate PDF
HTML(string=html_template).write_pdf(output_file)
print(f"PDF created: {output_file}")
