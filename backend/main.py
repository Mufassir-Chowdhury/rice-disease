

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

# Add CORS middleware
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

def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data))
    image = image.resize((256, 256))
    if image.mode == 'RGBA':
        # If image has alpha channel, remove it
        image = image.convert('RGB')
    return np.array(image)

@app.post("/predict")
def predict(file: UploadFile = File(...)):
    image = read_file_as_image(file.file.read())
    image = np.expand_dims(image, axis=0)
    prediction = MODEL.predict(image)
    return {
        "blight": round(float(prediction[0][0]), 3),
        "blast": round(float(prediction[0][1]), 3),
        "brownspot": round(float(prediction[0][2]), 3)
    }




