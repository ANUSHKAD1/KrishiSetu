from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__, static_folder="static", template_folder="templates")

# Load trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/")
def home():
    return render_template("index.html")  # serve frontend

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    features = np.array([[ 
        data["N"], 
        data["P"], 
        data["K"], 
        data["temperature"], 
        data["humidity"], 
        data["ph"], 
        data["rainfall"] 
    ]])
    
    prediction = model.predict(features)[0]
    return jsonify({"recommended_crop": prediction})

if __name__ == "__main__":
    app.run(debug=True,port=5004)
