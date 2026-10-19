import google.generativeai as genai
from PIL import Image
import json


def read_prescription(image, api_key):

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        'gemini-3.5-flash-lite'
    )

    image = Image.open(image)

    prompt = """
    Analyze this medical document carefully.

    If it is a prescription, extract ALL medicines.

    For every medicine, extract:
    - medicine name
    - dosage
    - frequency
    - duration

    Return ONLY valid JSON:

    {
        "patient_name": "",
        "doctor_name": "",
        "medicines": [
            {
                "name": "",
                "dosage": "",
                "frequency": "",
                "duration": ""
            }
        ]
    }

    IMPORTANT:
    - Read handwritten medicine names carefully.
    - Extract every medicine visible.
    - Do not return an empty medicines list when medicines are visible.
    - If dosage, frequency, or duration cannot be read, use "Not available".
    - Do not invent medicine names.
    """

    response = model.generate_content(
        [prompt, image]
    )

    text = response.text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    return json.loads(text)