from flask import Flask, render_template
import os
import pandas as pd

app = Flask(__name__)
DATA_DIR = "data"

def get_latest_csv(source_prefix):
    files = [f for f in os.listdir(DATA_DIR) if f.startswith(source_prefix) and f.endswith('.csv')]
    if not files:
        return None
    latest = max(files, key=lambda f: os.path.getctime(os.path.join(DATA_DIR, f)))
    return os.path.join(DATA_DIR, latest)

@app.route('/')
def index():
    central_csv = get_latest_csv('central')
    karnataka_csv = get_latest_csv('karnataka')

    central_table = pd.read_csv(central_csv).to_html(escape=False, classes="table table-striped") if central_csv else ""
    karnataka_table = pd.read_csv(karnataka_csv).to_html(escape=False, classes="table table-striped") if karnataka_csv else ""

    return render_template('index.html', central_table=central_table, karnataka_table=karnataka_table)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
