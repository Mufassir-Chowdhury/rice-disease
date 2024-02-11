from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model("./model/1")

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

@app.post("/predict")
def predict(file: UploadFile = File(...)):
    image = Image.open(BytesIO(file.file.read()))
    image = image.resize((256, 256))
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    prediction = MODEL.predict(image)
    return {
        "blight": round(float(prediction[0][0]), 3),
        "blast": round(float(prediction[0][1]), 3),
        "brownspot": round(float(prediction[0][2]), 3)
    }




