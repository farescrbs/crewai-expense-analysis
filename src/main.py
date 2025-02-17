from crewai import Agent, Task, Crew
from tools.custom_tool import search_knowledge_base
from src.utils.pdf_converter import convert_markdown_to_pdf


analyst = Agent(
    role="Expense Analyst",
    goal="Create detailed expense analysis and categorization from invoice data",
    backstory="""
        You are a meticulous expense analyst with expertise in financial data analysis
        and cost categorization. You excel at breaking down expenses, identifying patterns,
        and providing actionable cost-saving insights.
    """,
    verbose=True,
    tools=[search_knowledge_base],
)
reporter = Agent(
    role="Financial Reporter",
    goal="Write a clear and structured financial report based on expense analysis",
    backstory="""
        You are a skilled financial writer, specializing in turning raw data into
        professional, structured reports. Your mission is to make financial insights
        easy to understand and actionable.
    """,
    verbose=True,
)
compliance_auditor = Agent(
    role="Compliance Auditor",
    goal="Verify invoices for errors, fraud, and compliance issues",
    backstory="""
        You are a meticulous financial auditor with a keen eye for detail.
        Your role is to ensure invoices comply with company policies and detect 
        any inconsistencies, errors, or signs of fraud.
    """,
    verbose=True,
)
analysis_task = Task(
    description="""
        Search, find, and analyze invoices to create a detailed expense drilldown report.
        
        Steps to follow:
        1. Group expenses and calculate total spend by vendor.
        2. Calculate the gross total spend.
        3. Identify potential cost-saving opportunities.
        
        The report should include:
        - An executive summary.
        - A vendor-wise breakdown.
        - Recommendations for cost optimization.
    """,
    expected_output="""
        An expense analysis report with clear sections and actionable recommendations in markdown format.
    """,
    output_file="expense_report.md",
    agent=analyst,
)
write_report_task = Task(
    description="""
        Draft a well-structured financial report based on the expense analysis.

        **Instructions:**
        - Organize the report with an introduction, detailed analysis, and conclusion.
        - Summarize expenses by vendor.
        - Provide strategic cost-saving recommendations.
        - Format using Markdown with appropriate headings.

        **Suggested Sections:**
        1. Introduction
        2. Expense Analysis
        3. Vendor Breakdown
        4. Cost-Saving Opportunities
        5. Conclusion & Recommendations
    """,
    expected_output="A professional financial report in Markdown format.",
    output_file="final_expense_report.md",  # 📄 Save the final structured report
    agent=reporter,
)
audit_task = Task(
    description="""
        Review and verify invoices to identify errors, fraud, or compliance issues.

        **Steps:**
        1. Detect duplicate invoices.
        2. Check for abnormal amounts or suspicious patterns.
        3. Verify if all invoices follow company policies.
        4. Flag any issues and provide recommendations.

        **Expected output:**
        - A summary of all detected issues.
        - Recommended actions for correction.
    """,
    expected_output="A compliance audit report in Markdown format.",
    output_file="compliance_audit.md",
    agent=compliance_auditor,
)
# Convert Markdown reports to PDF after CrewAI execution
md_reports = ["compliance_audit.md", "expense_report.md", "final_expense_report.md"]

for md_file in md_reports:
    convert_markdown_to_pdf(md_file, output_folder="reports")

if __name__ == "__main__":
    crew = Crew(agents=[analyst, reporter, compliance_auditor], 
    tasks=[analysis_task, write_report_task, audit_task], verbose=True)
    crew.kickoff()