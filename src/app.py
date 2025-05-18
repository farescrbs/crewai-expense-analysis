import streamlit as st
import sys
import os
from pathlib import Path
import time
from dotenv import load_dotenv
import json

# Add src directory to Python path
current_dir = Path(__file__).parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))

from crewai import Agent, Task, Crew, Process
from src.tools.custom_tool import search_knowledge_base, access_memory
from crewai_tools import SerperDevTool

# Create uploads directory if it doesn't exist
upload_dir = current_dir / "uploads"
upload_dir.mkdir(exist_ok=True)

def create_crew():
    """Create and return the crew with all agents and tasks"""
    search_tool = SerperDevTool()

    supervisor = Agent(
        role="Supervisor",
        goal="Coordinate agents and ensure consistency of results",
        backstory="""
            You are an experienced supervisor in charge of coordinating the entire expense analysis workflow.
            Your responsibilities include:
            - Verifying consistency between different reports
            - Detecting anomalies in results
            - Relaunching analyses when necessary
            - Ensuring overall deliverable quality
            - Centralizing activity logging
            You have an excellent overview and know when to intervene to optimize the process.
        """,
        verbose=True
    )

    analyst = Agent(
        role="Expense Analyst",
        goal="Create detailed expense analysis and categorization from invoice data",
        backstory="""
            You are a meticulous expense analyst with expertise in financial data analysis
            and cost categorization. You excel at breaking down expenses, identifying patterns,
            and providing actionable cost-saving insights.
        """,
        verbose=True,
        tools=[search_knowledge_base, access_memory],
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
        tools=[search_knowledge_base, access_memory]
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
        tools=[search_knowledge_base, access_memory]
    )

    supplier_negotiator = Agent(
        role="Supplier Negotiator",
        goal="Find alternative suppliers with better pricing and negotiate discounts",
        backstory="""
            You are a skilled procurement specialist and negotiator. Your mission is to 
            identify alternative suppliers that offer similar products at lower costs 
            and negotiate with them to obtain the best possible deals.
        """,
        verbose=True,
        tools=[search_tool, access_memory],
    )

    analysis_task = Task(
        description="""
            Analyze all expense data to create a detailed breakdown report.
            
            Steps to follow:
            1. Group expenses by vendor
            2. Calculate total spend
            3. Identify cost-saving opportunities
            4. Compare with industry benchmarks
            
            The report should include:
            - Executive summary
            - Vendor-wise breakdown
            - Cost optimization recommendations
        """,
        expected_output="An expense analysis report with clear sections and actionable recommendations in markdown format.",
        output_file="expense_report.md",
        agent=analyst
    )

    write_report_task = Task(
        description="""
            Create a strategic financial report based on the expense analysis.

            Include:
            - Executive Summary
            - Detailed Expense Analysis
            - Trends & Anomalies
            - Strategic Recommendations
            - Next Steps
        """,
        expected_output="A clear, concise, and strategic financial report in Markdown format.",
        output_file="final_expense_report.md",
        agent=reporter,
        depends_on=[analysis_task]
    )

    audit_task = Task(
        description="""
            Review all invoices for compliance issues and potential fraud.

            Focus on:
            - Duplicate invoices
            - Unusual amounts
            - Policy violations
            - Suspicious patterns
        """,
        expected_output="A compliance audit report in Markdown format.",
        output_file="compliance_audit.md",
        agent=compliance_auditor,
        depends_on=[analysis_task]
    )

    find_and_negotiate_task = Task(
        description="""
            Find alternative suppliers and analyze cost-saving opportunities.

            Deliver:
            1. List of alternative suppliers
            2. Potential cost savings
            3. Negotiation recommendations
            4. Implementation plan
        """,
        expected_output="A supplier negotiation report in Markdown format.",
        output_file="negotiated_suppliers.md",
        agent=supplier_negotiator,
        depends_on=[analysis_task, audit_task]
    )

    supervision_task = Task(
        description="""
            Supervise the entire analysis process and ensure quality results.
            
            Tasks:
            1. Verify report consistency
            2. Validate recommendations
            3. Check calculations
            4. Ensure completeness
        """,
        expected_output="A supervision report in Markdown format.",
        output_file="supervision_report.md",
        agent=supervisor,
        depends_on=[analysis_task, write_report_task, audit_task, find_and_negotiate_task]
    )

    # Create Crew with hierarchical process
    crew = Crew(
        agents=[analyst, reporter, compliance_auditor, supplier_negotiator],
        tasks=[analysis_task, write_report_task, audit_task, find_and_negotiate_task, supervision_task],
        process=Process.hierarchical,
        manager_agent=supervisor,
        verbose=True
    )

    return crew

def save_api_keys(keys):
    """Save API keys to .env file"""
    with open('.env', 'w') as f:
        for key, value in keys.items():
            if value:  # Only write non-empty values
                f.write(f'{key}={value}\n')

def load_api_keys():
    """Load API keys from .env file"""
    load_dotenv()
    return {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', ''),
        'NEEDLE_API_KEY': os.getenv('NEEDLE_API_KEY', ''),
        'NEEDLE_COLLECTION_ID': os.getenv('NEEDLE_COLLECTION_ID', ''),
        'SERPER_API_KEY': os.getenv('SERPER_API_KEY', '')
    }

def main():
    st.set_page_config(
        page_title="AI Expense Analysis - Free Audit Tool",
        page_icon="📊",
        layout="wide"
    )

    # Header
    st.title("🤖 AI Expense Analysis Tool")
    st.markdown("""
    ### Free AI-Powered Expense Audit for Your Business
    This tool uses advanced AI agents to analyze your expenses, identify savings opportunities, 
    and negotiate with suppliers - all automatically!
    """)

    # Sidebar for API Configuration
    st.sidebar.title("⚙️ Configuration")
    
    # Load existing API keys
    api_keys = load_api_keys()
    
    # API Key inputs
    with st.sidebar.expander("🔑 API Keys Configuration", expanded=True):
        new_api_keys = {}
        new_api_keys['OPENAI_API_KEY'] = st.text_input(
            "OpenAI API Key",
            value=api_keys['OPENAI_API_KEY'],
            type="password"
        )
        new_api_keys['NEEDLE_API_KEY'] = st.text_input(
            "Needle API Key",
            value=api_keys['NEEDLE_API_KEY'],
            type="password"
        )
        new_api_keys['NEEDLE_COLLECTION_ID'] = st.text_input(
            "Needle Collection ID",
            value=api_keys['NEEDLE_COLLECTION_ID'],
            type="password"
        )
        new_api_keys['SERPER_API_KEY'] = st.text_input(
            "Serper API Key",
            value=api_keys['SERPER_API_KEY'],
            type="password"
        )
        
        if st.button("💾 Save API Keys"):
            save_api_keys(new_api_keys)
            st.success("API keys saved successfully!")

    # Main content area
    st.markdown("---")

    # File Upload Section
    st.header("📎 Upload Invoices")
    st.markdown("""
    Please upload your invoice files for analysis. Supported formats:
    - PDF
    - Excel (.xlsx, .xls)
    - CSV
    - Text (.txt)
    - Images (.jpg, .png)
    """)
    
    uploaded_files = st.file_uploader(
        "Drop your invoice files here",
        accept_multiple_files=True,
        type=['pdf', 'xlsx', 'xls', 'csv', 'jpg', 'png', 'txt']
    )

    if uploaded_files:
        # Save uploaded files
        for uploaded_file in uploaded_files:
            file_path = upload_dir / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ Successfully uploaded {len(uploaded_files)} files")
    else:
        st.info("⚠️ Please upload your invoice files before starting the analysis")

    # AI Agents Description
    st.markdown("---")
    with st.expander("🤖 Meet Your AI Analysis Team", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 📈 Expense Analyst
            Analyzes expenses, identifies patterns, and provides cost-saving insights.
            
            #### 📝 Financial Reporter
            Creates clear, structured reports from complex financial data.
            """)
            
        with col2:
            st.markdown("""
            #### 🔍 Compliance Auditor
            Checks for errors, fraud, and compliance issues.
            
            #### 💼 Supplier Negotiator
            Finds alternative suppliers and negotiates better prices.
            """)

    # Launch Analysis Section
    st.markdown("---")
    st.header("🚀 Launch Analysis")
    
    # Check if all required API keys are set and files are uploaded
    required_keys = ['OPENAI_API_KEY', 'NEEDLE_API_KEY', 'NEEDLE_COLLECTION_ID', 'SERPER_API_KEY']
    missing_keys = [key for key in required_keys if not new_api_keys.get(key)]
    
    if missing_keys:
        st.warning(f"⚠️ Please configure the following API keys first: {', '.join(missing_keys)}")
        st.stop()
    
    if not uploaded_files:
        st.warning("⚠️ Please upload invoice files before starting the analysis")
        st.stop()
    
    if st.button("🔄 Start Free Expense Analysis", type="primary", use_container_width=True):
        with st.spinner("🤖 AI Agents are analyzing your expenses... This may take several minutes."):
            # Progress indicators
            progress_placeholder = st.empty()
            report_placeholder = st.empty()
            
            progress_placeholder.markdown("""
            #### Current Progress:
            1. 📊 Processing uploaded files...
            2. 📈 Analyzing expenses...
            3. 🔍 Performing compliance checks...
            4. 💼 Negotiating with suppliers...
            5. 📝 Generating final reports...
            """)
            
            # Create and run the crew
            crew = create_crew()
            result = crew.kickoff()
            
            progress_placeholder.markdown("""
            #### Analysis Complete! ✅
            All reports have been generated successfully.
            """)
            
            st.success("🎉 Analysis completed successfully!")
            st.balloons()

    # Display Reports Section
    st.markdown("---")
    st.header("📑 Generated Reports")
    
    # List of reports
    reports = [
        ("expense_report.md", "📊 Expense Analysis"),
        ("final_expense_report.md", "📑 Final Report"),
        ("compliance_audit.md", "🔍 Compliance Audit"),
        ("negotiated_suppliers.md", "💼 Supplier Negotiations")
    ]
    
    # Create tabs for each report
    tabs = st.tabs([name for _, name in reports])
    
    for i, ((filename, _), tab) in enumerate(zip(reports, tabs)):
        with tab:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    st.markdown(content)
                    
                    # Download button for each report
                    st.download_button(
                        f"⬇️ Download {filename}",
                        content,
                        file_name=filename,
                        mime="text/markdown"
                    )
            except FileNotFoundError:
                st.info(f"No report generated yet. Run the analysis to generate {filename}.")

    # Footer
    st.markdown("---")
    st.markdown("""
    ### 💡 Need Help?
    - Make sure all API keys are properly configured
    - The analysis typically takes 5-10 minutes to complete
    - All reports are saved in Markdown format for easy sharing
    """)

if __name__ == "__main__":
    main() 