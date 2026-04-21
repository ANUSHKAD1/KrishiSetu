from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
encoders = pickle.load(open('label_encoders.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html', prediction=None, soil="", crop="")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form

    temp = float(data['temperature'])
    hum = float(data['humidity'])
    moisture = float(data['moisture'])
    soil = encoders['Soil Type'].transform([data['soil']])[0]
    crop = encoders['Crop Type'].transform([data['crop']])[0]
    n = float(data['nitrogen'])
    p = float(data['phosphorous'])
    k = float(data['potassium'])

    input_features = np.array([[temp, hum, moisture, soil, crop, n, p, k]])
    pred = model.predict(input_features)[0]
    fertilizer = encoders['Fertilizer Name'].inverse_transform([pred])[0]

    return render_template(
        'index.html',
        prediction=fertilizer,
        soil=data['soil'],
        crop=data['crop'],
        temperature=data['temperature'],
        humidity=data['humidity'],
        moisture=data['moisture'],
        nitrogen=data['nitrogen'],
        phosphorous=data['phosphorous'],
        potassium=data['potassium']
    )

if __name__ == '__main__':
    app.run(debug=True,port=5001)
