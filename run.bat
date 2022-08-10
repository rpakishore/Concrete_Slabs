:: cd C:\Users\rpaki\Documents\GitHub\Template-Python
cd /D "%~dp0"
@echo Started: %date% %time%
"venv\Scripts\activate.bat" && python -m streamlit run About.py