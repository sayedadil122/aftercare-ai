# AfterCare AI

AI-powered post-service recovery for repair businesses.

AfterCare AI automatically schedules a customer follow-up after a completed repair, uses CALL-E to check the customer's experience, analyzes the conversation, calculates risk, and creates a ticket/recovery case when service issues are detected.

## Core flow

1. Completed repair is captured.
2. Follow-up is scheduled based on repair type.
3. CALL-E places the follow-up call.
4. AI analyzes the conversation for issue, severity, sentiment, safety and warranty relevance.
5. Risk is scored and the appropriate recovery action is created.
6. Dashboard surfaces customer health, tickets and recovery operations.

## Tech stack

- Python
- Streamlit
- Pandas
- Plotly
- CALL-E Python SDK (`calle-ai==0.2.0`)
- CSV-based demo data

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Create a local `.env` file from `.env.example` and add your CALL-E API key.

## Streamlit Cloud

Add `CALLE_API_KEY` in the app's Streamlit Secrets before using live CALL-E calls. Never commit `.env` or API keys to GitHub.

The app can also be used in simulation mode without placing a real call.

## Live calling

CALL-E supports India (IN) with English and Hindi. Live outbound calls require the appropriate CALL-E account/number setup and permissions.

## Repository

Built as an AI Product Manager portfolio project focused on proactive service recovery and customer experience.
