from flask import Flask, request, json
import boto3
import pickle

BUCKET_NAME = 'covid-teamtwo-models'
MODEL = 'uk_change_estimator'

app = Flask(__name__)

S3 = boto3.client('s3', region_name = 'eu-west-1')

@app.route('/', methods = ['POST'])
def index():
    
    body = request.get_json(silent=True)
    data = body['data']

    model = load_model(MODEL)
    prediction = model.predict(data).tolist()

    result = {'prediction': prediction}

    return json.dumps(result)

def load_model(model_name):

    #TODO refactor
    response = S3.get_object(Bucket=BUCKET_NAME, Key=model_name)
    model_str = response['Body'].read()
    model = pickle.loads(model_str)

    return model

if __name__ == '__main__':
    app.run(host='0.0.0.0')