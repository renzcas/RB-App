from flask import Flask, jsonify, render_template_string
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to RB-App cockpit!"

@app.route("/hello")
def hello():
    return "Hello, recruiter! This is a test route."

@app.route("/data")
def data():
    log_path = os.path.join(os.path.dirname(__file__), "data", "logger.py")
    records = []
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    timestamp, event, value = parts
                    try:
                        value = float(value)
                        records.append({"timestamp": timestamp, "event": event, "value": value})
                    except ValueError:
                        pass
    return jsonify(records)

@app.route("/dashboard")
def dashboard():
    html_template = """ (your HTML stays exactly as-is) """
    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(debug=True)