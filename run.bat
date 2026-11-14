@echo off
start "Backend" cmd /k "cd /d %~dp0backend && .venv\Scripts\activate && uvicorn app.main:app --reload"
cd /d %~dp0frontend
streamlit run main.py