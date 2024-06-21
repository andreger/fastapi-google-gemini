# Build a Text Generation and Image Analysis API with FastAPI and Gemini AI

This tutorial guides you through creating an API using FastAPI that interacts with Google's Gemini AI models. The API will offer two main functionalities:

* **generate_text:** This endpoint receives a text prompt and uses Gemini to generate text based on it.
* **image_to_text:** This endpoint receives an image URL and uses Gemini to extract text from it.

## About the author - André Gervásio

20+ years of experience in software development. Bachelor's degree in Computer Science. Fullstack Software Engineer and Tech Lead in Java, Python, JS, PHP applications. Certified in Front-End, Back-End and DevOps technologies. Experienced in Scrum and Agile Methodologies. Solid knowledge in Databases and ORMs. Practical skills in Cloud Computing Services.

## 1. Set Up Python and FastAPI

Before we start coding, make sure you have the necessary tools installed:

Check if Python is installed by running the following command in your terminal:

  ```bash
  python3 --version # or python --version
  ```

  If Python is installed, you'll see the version number. Otherwise, download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).

Next, create a directory for your project. In this example, we'll name it fastapi-google-gemini. Navigate to this directory and set up a virtual environment to manage project dependencies:

  ```bash
  mkdir fastapi-google-gemini
  cd fastapi-google-gemini
  python3 -m venv venv
  ```

Activate your virtual environment:


  ```bash
  source venv/bin/activate
  ```

Now, install FastAPI using pip:

  ```bash
  pip install fastapi
  ```

## 2. Integrate Google GenerativeAI Library

The Google GenerativeAI library allows us to interact with the Gemini API for generating responses.

Use pip to install the library:

  ```bash
  pip install google-generativeai
  ```

* **Obtain a Gemini API key:**

An API key is required to use the GenerativeAI library. See this article to learn [how to generate a Gemini API key](http://localhost:13000/post/how-to-generate-a-gemini-api-key)

We'll use an environment variable for security. In your terminal, set the API key using a command like:

  ```bash
  export GENERATIVE_AI_KEY="YOUR_API_KEY_HERE"
  ```

Replace `YOUR_API_KEY_HERE` with your actual key.

## 3. Create a FastAPI App

Inside your project directory, create a new Python file named main.py.

```python
from fastapi import FastAPI
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GENERATIVE_AI_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

app = FastAPI()
```

This code sets up a FastAPI web application and configures it to interact with Gemini AI models. It imports libraries for building the API (FastAPI) and interacting with Gemini (google-generativeai). It also retrieves your Gemini API key from an environment variable for secure authentication.

## 4. Create the generate_text endpoint

In the main.py file, import the required libraries.

```python
from pydantic import BaseModel
```

Define a data model to represent a text input.

```python
class TextInput(BaseModel):
    prompt: str
```

Create a new route for the generate_text endpoint.

```python
@app.post("/generate_text")
def generate_text(input: TextInput):
    """Generates text based on the provided prompt."""

    response = model.generate_content(input.prompt)
    return {"generated_text": response.text}
```

  This code receives a user prompt via a POST request. It then uses the `google-generativeai` library to interact with a Gemini text generation model and generate text based on the prompt. Finally, it returns the generated text as a JSON response.

Expected input example:

```json
{
  "prompt": "What is the meaning of life?"
}
```

## 5. Create the image_to_text endpoint

We need to install pillow library for image processing. Install it using pip:

```bash
pip install pillow
```

In the main.py file, import the required libraries.

```python
import urllib.request
from PIL import Image
import tempfile
```

Define a data model to represent an image input.

```python
class ImageInput(BaseModel):
    url: str
```

Create a new route for the image_to_text endpoint.

```python
@app.post("/image_to_text")
def image_to_text(input: ImageInput):
    """Extracts text from an image."""

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        urllib.request.urlretrieve(input.url, temp_file.name)
        img = Image.open(temp_file.name)
        response = model.generate_content(["What is in this photo?", img])
    temp_file.close()

    return {"generated_text": response.text}
```

This function takes an image URL, downloads it to a temporary file, opens the image, uses a model to analyze it and generate text description, cleans up the temporary file, and returns the generated text.

Expected input example:

```json
{
  "url": "https://www.nasa.gov/wp-content/themes/nasa/assets/images/nasa-logo.svg"
}
```


## 6. Run the FastAPI Server and Test the API

Run the FastAPI development server using the following command in your terminal:

```bash
fastapi dev main.py  # for production use: fastapi run main.py
```

FastAPI automatically generates interactive documentation for your API using Swagger. To access the documentation, navigate to http://localhost:8000/docs in your web browser. This interface provides a user-friendly way to explore your API

Within the Swagger UI, you can directly test each endpoint by providing the necessary input data and clicking the "Execute" button. This allows you to verify if the API responds as expected for different inputs.

## Conclusion

This tutorial has guided you through creating a FastAPI API that interacts with Google's Gemini AI models using the `google-generativeai` library. The API offers two functionalities: generating text based on prompts and extracting text from images. Remember to replace placeholders with your actual Gemini API key and project details. With this API and the testing methods mentioned above, you can ensure its functionality and leverage the power of Gemini to create innovative applications.
