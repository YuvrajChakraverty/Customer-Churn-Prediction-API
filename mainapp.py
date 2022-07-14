from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

def columns_add_remove(data):
    
    def tenure_cohort(tenure_months):
        if tenure_months < 13:
            return '0-12 Months'
        elif tenure_months < 25:
            return '12-24 Months'
        elif tenure_months < 49:
            return '24-48 Months'
        else:
            return "Over 48 Months"
    
    data['Tenure Cohort'] = data['tenure'].apply(tenure_cohort)
    
    data=data.drop('customerID',axis=1)
    
    return data

# @app.route('/', methods=['GET'])
# def ping():
#     return "Application Working!"

@app.route('/predict', methods=['POST'])
def predict():
    
    feat_data = request.json
    df = pd.DataFrame(feat_data)
    df = df.reindex(columns=col_names)
    prediction = list(model.predict(df))
    return jsonify({'prediction': str(prediction)})


if __name__ == '__main__':
    with open('Customer Churn Prediction Model.pkl', 'rb') as f_in:
        model = pickle.load(f_in)
    with open('Customer Churn Prediction Columns.pkl', 'rb') as f_in:
        col_names = pickle.load(f_in)