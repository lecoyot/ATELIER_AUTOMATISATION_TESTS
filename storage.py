
import sqlite3
import json
from datetime import datetime

DATABASE_FILE = 'test_history.db'

def _get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def init_db():
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            summary_json TEXT NOT NULL,
            tests_json TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_run(run_data):
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO test_runs (api_name, timestamp, summary_json, tests_json) VALUES (?, ?, ?, ?)",
        (
            run_data['api'],
            run_data['timestamp'],
            json.dumps(run_data['summary']),
            json.dumps(run_data['tests'])
        )
    )
    conn.commit()
    conn.close()
    print(f"Test run saved at {run_data['timestamp']}")

def get_all_runs():
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_runs ORDER BY timestamp DESC")
    runs = cursor.fetchall()
    conn.close()
    return [
        {
            'id': run['id'],
            'api': run['api_name'],
            'timestamp': run['timestamp'],
            'summary': json.loads(run['summary_json']),
            'tests': json.loads(run['tests_json'])
        }
        for run in runs
    ]

def get_latest_run():
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_runs ORDER BY timestamp DESC LIMIT 1")
    run = cursor.fetchone()
    conn.close()
    if run:
        return {
            'id': run['id'],
            'api': run['api_name'],
            'timestamp': run['timestamp'],
            'summary': json.loads(run['summary_json']),
            'tests': json.loads(run['tests_json'])
        }
    return None

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
    # Example usage:
    # from tester.runner import TestRunner
    # runner = TestRunner()
    # run_results = runner.run_all_tests()
    # save_run(run_results)
