from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image
import google.generativeai as genai
import os, tempfile,urllib.request

genai.configure(api_key=os.getenv("GENERATIVE_AI_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

class TextInput(BaseModel):
    prompt: str

class ImageInput(BaseModel):
    url: str

app = FastAPI()

@app.post("/generate_text")
def generate_text(input: TextInput):
    """Generates text based on the provided prompt."""

    response = model.generate_content(input.prompt)
    return {"generated_text": response.text}

@app.post("/image_to_text")
def image_to_text(input: ImageInput):
    """Extracts text from an image."""

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        urllib.request.urlretrieve(input.url, temp_file.name)
        img = Image.open(temp_file.name)
        response = model.generate_content(["What is in this photo?", img])
    temp_file.close()   

    return {"generated_text": response.text}