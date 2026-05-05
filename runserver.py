import os
from park import create_app  # ИСПРАВЛЕНО: импортируем из park, а не park.app
from park.extensions import db

app = create_app()

if __name__ == "__main__":
    # Гарантируем наличие папки instance перед запуском
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
        print(f"✅ Создана папка: {instance_path}")

    with app.app_context():
        try:
            # Если seed_data.py уже сработал, эта строка просто проверит связь
            db.create_all()
            print("✅ Подключение к базе данных успешно")
        except Exception as e:
            print(f"❌ Ошибка базы данных: {e}")
            print("Совет: Попробуйте закрыть все программы, которые могут использовать park.db")

    app.run(debug=True)