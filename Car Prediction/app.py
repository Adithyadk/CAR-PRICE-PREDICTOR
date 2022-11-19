from flask import Flask, render_template, request
from flask import jsonify
import pickle
import numpy as np
import pandas as pd
# import sklearn
# from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('linearRegressionModel.pkl', 'rb'))
cardata = pd.read_csv('Cleaned Dataset.csv')
name = sorted(cardata['name'].unique())
#print(name)
#print(cardata)


@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html', carname=name)


# standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    fuel_Diesel = 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Km_driven = int(request.form['km_driven'])
        Km_driven2 = np.log(Km_driven)
        #Owner = int(request.form['owner'])
        fuel_Petrol = request.form['fuel_Petrol']
        if (fuel_Petrol == 'Petrol'):
                fuel_Petrol = 1
                fuel_Diesel = 0
                fuel_LPG = 0
                fuel_CNG = 0
                fuel_Electric = 0

        elif (fuel_Petrol == 'Diesel'):
                fuel_Petrol = 0
                fuel_Diesel = 1
                fuel_LPG = 0
                fuel_CNG = 0
                fuel_Electric = 0

        elif (fuel_Petrol == 'LPG'):
                fuel_Petrol = 0
                fuel_Diesel = 0
                fuel_LPG = 1
                fuel_CNG = 0
                fuel_Electric = 0

        elif (fuel_Petrol == 'CNG'):
                fuel_Petrol = 0
                fuel_Diesel = 0
                fuel_LPG = 0
                fuel_CNG = 1
                fuel_Electric = 0
        else:
                fuel_Petrol = 0
                fuel_Diesel = 0
                fuel_LPG = 0
                fuel_CNG = 0
                fuel_Electric = 1
                Year = 2022-Year

        Seller_Type_Individual = request.form['seller_type_Individual']
        if (Seller_Type_Individual == 'Individual'):
            seller_type_Individual = 1
            seller_type_Dealer = 0
            seller_type_Trustmark_Dealer = 0

        elif (Seller_Type_Individual == 'Dealer'):
            seller_type_Individual = 0
            seller_type_Dealer = 1
            seller_type_Trustmark_Dealer = 0

        else:
             seller_type_Individual = 0
             seller_type_Dealer = 0
             seller_type_Trustmark_Dealer = 1

        Transmission_Manual = request.form['transmission_Manual']
        if (Transmission_Manual == 'Manual'):
            transmission_Manual = 1
        else:
            transmission_Manual = 0
        Owner = int(request.form['owner'])
        #prediction=model.predict([[name,Km_driven2,Owner,Year,fuel_Petrol,seller_type_Individual,Transmission_Manual]])
        ls=['Hyundai Xcent 1.2',2016,25000,'Petrol','Individual','Manual','First Owner']
        final_features = [np.array(ls)]
        print (final_features)
        prediction = model.predict(final_features)
        #prediction=model.predict(ls)
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

