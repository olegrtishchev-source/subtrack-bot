import os

structure = [
    "venv/",
    "src/",
    "src/__init__.py",
    "src/main.py",
    "src/config.py",
    "src/services/",
    "src/services/__init__.py",
    "src/services/tinkoff_api.py",
    "src/models/",
    "src/models/__init__.py",
    "src/models/database.py",
    "src/utils/",
    "src/utils/__init__.py",
    "src/utils/logger.py",
    "requirements.txt",
    "README.md",
    "Dockerfile",
    "docker-compose.yml"
]

print("Создаю структуру проекта...")

for item in structure:
    if item.endswith('/'):
        os.makedirs(item, exist_ok=True)
        print(f"Создана папка: {item}")
    else:
        with open(item, 'w', encoding='utf-8') as f:
            pass
        print(f"Создан файл: {item}")

print("Структура проекта создана!")
