# app.py

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS # Import CORS
# Import the functions from your other script
from processing_script import analyze_farm_health, generate_status_message, send_sms_alert
import os

# Tell Flask where to find the HTML files
template_dir = os.path.abspath('../Frontend')
app = Flask(__name__, template_folder=template_dir)
CORS(app) # Enable CORS for all routes

@app.route('/')
def home():
    """
    This function serves the main HTML page to the user.
    """
    return render_template('index.html')

# --- API ENDPOINT ---
@app.route('/trigger-analysis', methods=['POST'])
def trigger_analysis():
    """
    This endpoint is called by the frontend JavaScript.
    It receives latitude and longitude, runs the full analysis,
    and sends the SMS.
    """
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')

    if not lat or not lon:
        return jsonify({'status': 'error', 'message': 'Latitude and Longitude are required.'}), 400

    try:
        # 1. Analyze the farm using Google Earth Engine
        avg_ndvi = analyze_farm_health(float(lon), float(lat))

        # 2. Generate the status message
        report_message = generate_status_message(avg_ndvi)

        # 3. Send the report as an SMS alert via Twilio
        send_sms_alert(report_message)

        # 4. Return a success response to the frontend
        response_data = {
            'status': 'success',
            'message': 'Analysis complete and SMS sent!',
            'report': report_message
        }
        return jsonify(response_data)

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    # This runs the web server on your local machine.
    # You can access it by going to http://127.0.0.1:5000 in your browser.
    app.run(debug=True, port=5000)
