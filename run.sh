#!/bin/bash
echo "Установка зависимостей..."
pip install -r requirements.txt

echo "Получение данных..."
python fetch_issues.py

echo "Запуск тестов..."
pytest

echo "Запуск графиков"
python process_data.py