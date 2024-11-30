Для автоматического запуска выполните следующее действие:
Для Linux введите команды:
1. 
```bash
chmod +x install.sh
```
2. 
```bash
./run.sh
```

Для Windows:
1. запустите run.bat


Для ручного запуска последовательно выполните следующие команды: 
Создание виртуальной среды:
```bash
python -m venv ./venv
```
Вход в виртуальную среду:
```bash
. ./venv/bin/activate
```

Установка библиотек:
```bash
pip install -r requirements.txt
```

Получение данных:
```bash
python fetch_issues.py
```

Запуск графиков:
```bash
python process_data.py
```
