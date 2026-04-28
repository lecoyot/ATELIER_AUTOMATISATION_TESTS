
from flask import Flask, render_template
import sys
import os

# Add the parent directory of storage.py to the Python path
# This assumes flask_app.py is in ATELIER_AUTOMATISATION_TESTS/ and storage.py is in ATELIER_AUTOMATISATION_TESTS/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import storage
from tester.runner import TestRunner

app = Flask(__name__)

# Initialize the database when the app starts
with app.app_context():
    storage.init_db()

@app.route('/')
def index():
    return 'Hello from Flask! API Testing Dashboard coming soon.'

@app.route('/dashboard')
def dashboard():
    latest_run = storage.get_latest_run()
    all_runs = storage.get_all_runs()
    return render_template('dashboard.html', latest_run=latest_run, all_runs=all_runs, message='Latest test results:')

@app.route('/run')
def run_tests():
    runner = TestRunner()
    run_results = runner.run_all_tests()
    storage.save_run(run_results)
    # Redirect to dashboard after running tests
    from flask import redirect, url_for
    return redirect(url_for('dashboard'))
