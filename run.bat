@echo off
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Getting data..."
python fetch_issues.py

echo "Launching charts"
python process_data.py