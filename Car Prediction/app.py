from flask import Flask, render_template, request
from flask import jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)
cardata = pd.read_csv('Cleaned Dataset.csv')
name = sorted(cardata['name'].unique())
from sklearn import preprocessing
model = pickle.load(open("model.pkl", "rb"))
dataset = pd.read_csv("orderedcarset2.csv")
name = sorted(dataset['name'].unique())
tran=pickle.load(open("trans.pkl","rb"))
@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html', carname=name)



@app.route("/predict", methods=['POST'])
def predict():
    car_name = request.form['name']
    year = request.form['year']
    fuel_type = request.form['fuel_type']
    seller = request.form['seller_type']
    trans = request.form['transmission']
    owner = request.form['owner']
    driven = request.form['km_driven']
    
    data=np.array([car_name, fuel_type, seller, trans, owner, int(year),int(driven)])
    print(data)
    t=tran.transform(pd.DataFrame(columns=['name', 'fuel', 'seller_type', 'transmission', 'owner', 'year','km_driven'],data=[data]))
    
    prediction = model.predict(t)

    print(prediction)

    return render_template('index.html',carname=name,prediction_text=str(np.round(prediction[0], 2)))


if __name__=="__main__":
    app.run(debug=True)

