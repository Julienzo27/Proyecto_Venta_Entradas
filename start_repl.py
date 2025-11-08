import os
from create_db import init_db


def main():
    # Ensure DB exists and is seeded before importing the app
    db_path = os.environ.get('DB_PATH', 'db.sqlite3')
    init_db(db_path)

    # Import app after DB is ready
    from app import app

    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    main()
