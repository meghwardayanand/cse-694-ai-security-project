import os

from dotenv import load_dotenv


load_dotenv()  # loads .env if present

from safe_sql_module import is_safe_sql, sanitize_sql


def demo_sanitizer():
    tests = [
        "SELECT * FROM users WHERE username = 'alice';",
        "SELECT * FROM users WHERE username = 'admin' OR '1'='1'; --",
        "DROP TABLE users;",
        "SELECT name FROM products WHERE id = 1;",
        "' OR 1=1 --",
        "' OR '1'='1",
        "admin' OR '1'='1' --",
        "' OR ''='",
        "admin' --",
        "admin' OR '1'='1'/*",
        "' OR 1=1 LIMIT 1 --",
        "' OR TRUE --",
        "'; DROP TABLE users; --",
        "'; UPDATE users SET role='admin' WHERE username='test'; --",
        "1; DROP DATABASE testdb; --",
        "' UNION SELECT 1,2,3 --",
        "' UNION SELECT username, password, 1 FROM users --",
        "' UNION SELECT name FROM sqlite_master WHERE type='table' --",
        "' UNION SELECT sql FROM sqlite_master --",
        "' OR 1=1; SELECT sleep(5); --",
        "' OR 1=1; WAITFOR DELAY '00:00:05'; --",
        "1 OR 1=1",
        "1 OR TRUE",
        "0 UNION SELECT 1, 'test', 3 --",
        "' ; DELETE FROM users WHERE id > 0; --",
        "' ; UPDATE users SET password='hacked'; --",
        "' UNION SELECT sql FROM sqlite_master WHERE tbl_name='users' --",
    ]
    for q in tests:
        try:
            clean = sanitize_sql(q)
            print(f"[OK] Safe: {clean}")
        except Exception as e:
            print(f"[BLOCKED] Query blocked: {q!r}  Reason: {e}")

if __name__ == "__main__":
    print("=== Running sanitizer demo ===")
    demo_sanitizer()

    try:
        db_url = os.environ.get("DATABASE_URL", "sqlite:///./demo.db")
        print("Creating SQLDatabase (for demonstration only) at", db_url)

        from safe_sql_module import SafeSQLDatabase
        safe_db = SafeSQLDatabase.from_uri(db_url)
        print("SafeSQLDatabase created (demo).")
    except Exception as e:
        print("LangChain not available or DB init failed (that's fine for sanitizer demo).", e)
