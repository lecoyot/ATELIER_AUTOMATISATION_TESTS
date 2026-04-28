
from flask import Flask, render_template, request, redirect, url_for
import storage
from tester import runner
import json # Added import for json

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/run')
def run_tests_endpoint():
    # Initialize database if not already done (redundant if storage.py init_db() works)
    storage.init_db()
    
    # Run the tests
    test_results = runner.run_tests()
    
    # Save the results to the database
    storage.save_run(test_results)
    
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # Retrieve all runs from the database
    all_runs = storage.list_runs(limit=20) # Display last 20 runs
    
    # Ensure results are loaded as JSON if stored as text
    for run in all_runs:
        if isinstance(run.get('results'), str):
            run['results'] = json.loads(run['results']) # from json import json 
            
    return render_template('dashboard.html', runs=all_runs)

# NOTE: For local development, you'd typically use:
# if __name__ == '__main__':
#    app.run(debug=True)

# On PythonAnywhere, the WSGI file will handle running the app.
