# Automated Expense Analysis with CrewAI

This project uses CrewAI to automatically analyze expenses from invoices and generate detailed reports.

## 🚀 Setup

1. Clone the repository
2. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/MacOS
.\venv\Scripts\activate   # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables in a `.env` file:
```env
OPENAI_API_KEY="your-openai-key"
NEEDLE_API_KEY="your-needle-key"
NEEDLE_COLLECTION_ID="your-collection-id"
```

## 📊 Usage

To run the expense analysis:

```bash
python src/main.py
```

The program will generate two files:
- `expense_report.md`: Initial expense analysis report
- `final_expense_report.md`: Structured final report

## 🤖 Features

The system uses two AI agents:
1. **Expense Analyst**: Analyzes invoices and identifies trends
2. **Financial Reporter**: Transforms the analysis into a structured report

## 📝 Project Structure

```
.
├── src/
│   ├── main.py           # Main script
│   └── tools/            # Custom tools
│       └── custom_tool.py
├── requirements.txt      # Python dependencies
└── .env                 # Environment variables
```

## 🔑 Prerequisites

- Python 3.8+
- OpenAI API Key
- Needle API Key
- Needle Collection ID 