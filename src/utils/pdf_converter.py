import os
import markdown2
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

def generate_charts(data, output_folder):
    """
    Generates financial charts (pie chart & bar chart) and saves them as images.
    
    Args:
        data (dict): Expense data by vendor.
        output_folder (str): Folder to save charts.
    """
    os.makedirs(output_folder, exist_ok=True)

    # Convert data to DataFrame
    df = pd.DataFrame(list(data.items()), columns=['Vendor', 'Total Expense'])

    # Pie Chart
    pie_chart_path = os.path.join(output_folder, "expense_pie_chart.png")
    plt.figure(figsize=(5, 5))
    plt.pie(df["Total Expense"], labels=df["Vendor"], autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    plt.title("Expense Distribution by Vendor")
    plt.savefig(pie_chart_path)
    plt.close()

    # Bar Chart
    bar_chart_path = os.path.join(output_folder, "expense_bar_chart.png")
    plt.figure(figsize=(6, 4))
    plt.bar(df["Vendor"], df["Total Expense"], color=plt.cm.Paired.colors)
    plt.xlabel("Vendor")
    plt.ylabel("Total Expense ($)")
    plt.title("Expense per Vendor")
    plt.xticks(rotation=45)
    plt.savefig(bar_chart_path)
    plt.close()

    return pie_chart_path, bar_chart_path

def convert_markdown_to_pdf(md_file: str, output_folder: str = "reports", expense_data=None):
    """
    Converts a Markdown file to a well-formatted PDF with tables and charts.
    
    Args:
        md_file (str): Path to the Markdown file.
        output_folder (str): Folder where the PDF will be stored.
        expense_data (dict): Expense data for generating tables and charts.
    """
    os.makedirs(output_folder, exist_ok=True)

    # Read Markdown content
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown2.markdown(md_content)

    # Define PDF output path
    pdf_filename = os.path.splitext(os.path.basename(md_file))[0] + ".pdf"
    pdf_path = os.path.join(output_folder, pdf_filename)

    # Create PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('TitleStyle', parent=styles['Title'], fontSize=16, textColor=colors.darkblue, spaceAfter=10)
    subtitle_style = ParagraphStyle('SubtitleStyle', parent=styles['Heading2'], fontSize=12, textColor=colors.black, spaceAfter=8)
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontSize=10, leading=14)

    elements = []

    # Add content from Markdown
    for line in html_content.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            elements.append(Paragraph(line[2:], title_style))
        elif line.startswith("## "):
            elements.append(Paragraph(line[3:], subtitle_style))
        else:
            elements.append(Paragraph(line, normal_style))
        elements.append(Spacer(1, 10))

    # Add Expense Table if Data Available
    if expense_data:
        data = [["Vendor", "Total Expense ($)"]]
        for vendor, expense in expense_data.items():
            data.append([vendor, f"${expense:,.2f}"])

        table = Table(data, colWidths=[200, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(Paragraph("Expense Breakdown", subtitle_style))
        elements.append(table)
        elements.append(Spacer(1, 20))

        # Generate and Add Charts
        pie_chart_path, bar_chart_path = generate_charts(expense_data, output_folder)
        elements.append(Image(pie_chart_path, width=300, height=300))
        elements.append(Spacer(1, 20))
        elements.append(Image(bar_chart_path, width=400, height=250))

    # Build PDF
    doc.build(elements)

    print(f"✅ PDF saved at: {pdf_path}")
