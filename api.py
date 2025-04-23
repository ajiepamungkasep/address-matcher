from fastapi import FastAPI
import pandas as pd
import numpy as np

from tensorflow import keras
import joblib

app = FastAPI()

VECTORIZER_PATH = "app/models/vectorizer.pkl" 
MODEL_PATH = 'app/models/DeepLearning.h5'
ADDRESS_PATH = 'app/CodexToAddress.csv'

class AddressDetector:
    def __init__(self):
        print("start load model")
        self.vectorizer = self.get_vectorizer()
        self.model = self.get_model()
        self.address = self.get_address()
        print("end load model")

    def get_vectorizer(self):
        return joblib.load(VECTORIZER_PATH)

    def get_model(self):
        return keras.models.load_model(MODEL_PATH)

    def get_address(self):
        df = pd.read_csv(ADDRESS_PATH,delimiter=";", index_col='Codex')
        df.drop('Unnamed: 0', axis=1, inplace=True)
        return df

    def search(self, address: list):
        naddress = self.vectorizer.transform(address).toarray()
        prediction = self.model.predict(naddress)
        df = address_detector.address
        sort=np.argsort(-prediction, axis=1)
        argSort=sort[0,0:5]
        result=df.loc[argSort].copy()
        confidence=prediction[0,argSort]
        portion=confidence/np.sum(confidence)
        result['confidence']=portion
        return result

address_detector = AddressDetector()

@app.get("/")
async def root(address):
    result = address_detector.search([address])
    return result.head(n=5).to_dict('records')
