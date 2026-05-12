# Chat with Customer Data

A simple tool to ask questions about Excel data using AI.

## What it does

- Upload any Excel file
- Ask questions in plain English
- Get answers based on your data

## How it works

1. User uploads an Excel file
2. User types a question like "How many customers have budget above 90 lakhs?"
3. The app uses Gemini AI to understand the question
4. It converts the question to Python code
5. Runs the code on your data
6. Shows the answer

## Files in this project

```
chat-with-customer-data/
├── app.py              # Main application
├── query_engine.py     # Handles AI and data processing
├── data_loader.py      # Loads Excel files
├── requirements.txt    # Required packages
└── README.md           # This file
```

## How to setup and run

Get free API key from: https://makersuite.google.com/app/apikey

**For Mac/Linux:**
```bash
git clone https://github.com/Arpita-Sarda/arpitasarda45-chat_with_customer_data
cd chat_with_customer_data
python3 -m venv myenv
source venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY="your_api_key_here"
streamlit run app.py
```

**For Windows (Command Prompt):**
```bash
git clone https://github.com/Arpita-Sarda/arpitasarda45-chat_with_customer_data
cd chat_with_customer_data
python -m venv myenv
venv\Scripts\activate
pip install -r requirements.txt
set GEMINI_API_KEY=your_api_key_here
streamlit run app.py
```

App opens at http://localhost:8501

## How to use

1. Click "Browse files" and select your Excel file
2. Type your question
3. Click "Get Answer"
4. See the result

## Example questions

- How many records are there?
- What is the average budget?
- List customers in Pune
- How many customers have budget above 50 lakhs?
- Which location has the most customers?

## Technologies used

- Python
- Streamlit
- Pandas
- Google Gemini AI
