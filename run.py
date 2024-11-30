import subprocess
import sys

def install():
    """Устанавливает зависимости"""
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def test():
    """Запускает тесты"""
    subprocess.run(["pytest", "tests"])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Скрипт управления проектом")
    parser.add_argument("command", choices=["install", "lint", "test"], help="Команда для выполнения")
    args = parser.parse_args()

    if args.command == "install":
        install()
    elif args.command == "test":
        test()
