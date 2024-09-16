# import numpy as np
# import joblib
# from flask import Flask, request, jsonify

# model = joblib.load('trained_model.pkl')


# def encode_owner(owner):
#     if owner == 'First Owner':
#         return [1.0, 0.0, 0.0]
#     elif owner == 'Second Owner':
#         return [0.0, 1.0, 0.0]
#     elif owner == 'Third Owner':
#         return [0.0, 0.0, 1.0]
#     else:
#         raise ValueError("Invalid owner type. Choose from 'First', 'Second', or 'Third'.")

# def encode_fuel_type(fuel_type):
#     if fuel_type == 'Petrol':
#         return 1
#     elif fuel_type == 'Diesel':
#         return 0
#     else:
#         raise ValueError("Invalid fuel type. Choose 'Petrol' or 'Diesel'.")

# def encode_deal_type(deal_type):
#     if deal_type == 'Individual':
#         return 1
#     elif deal_type == 'Dealer':
#         return 0
#     else:
#         raise ValueError("Invalid deal type. Choose 'Individual' or 'Dealer'.")

# def encode_transmission_type(transmission_type):
#     if transmission_type == 'Manual':
#         return 1
#     elif transmission_type == 'Automatic':
#         return 0
#     else:
#         raise ValueError("Invalid transmission type. Choose 'Manual' or 'Automatic'.")


# app = Flask(__name__)

# @app.route('/submit', methods=['POST'])
# def handle_data():
#     # Receive data from the form
#     owner_type = request.form['owner']
#     fuel_type = request.form['fuel_type']
#     deal_type = request.form['deal_type']
#     transmission_type = request.form['transmission']
#     year = int(request.form['year'])
#     mileage = float(request.form['mileage'])
#     engine_size = float(request.form['engine_size'])
#     power = float(request.form['power'])
#     seats = float(request.form['seats'])
#     kilometer_driven = float(request.form['kilometer_driven'])
    
#     owner = encode_owner(owner_type)
#     fuel = encode_fuel_type(fuel_type)
#     deal = encode_deal_type(deal_type)
#     transmission = encode_transmission_type(transmission_type)
    
#     input_features = owner + [year, kilometer_driven, fuel, deal, transmission, power, mileage, engine_size, seats]
#     print(input_features)
    
#     # Make prediction
#     output = model.predict([input_features])[0]

#     # Return the prediction as JSON
#     return jsonify({'prediction': output})

#     if __name__ == '__main__':
#     # app.run(debug=True)

#     # owner = encode_owner(owner_type)
# # fuel = encode_fuel_type(fuel_type)
# # deal = encode_deal_type(deal_type)
# # transmission = encode_transmission_type(transmission_type)
# # year = 2020
# # mileage = 50
# # kilometer_driven = 100
# # engine_size = 1348.0
# # power = 100
# # seats = 5.0

# # input_features = owner + [year, kilometer_driven, fuel, deal, transmission, power, mileage, engine_size, seats]
# # print(input_features)

# # output = model.predict([input_features])
# # output