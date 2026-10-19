from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv

import io
import os

from database import (
    create_database,
    save_prescription,
    get_prescriptions
)

from prescription_reader import read_prescription
from location import get_location
from pharmacy import find_pharmacies
from medigrid_warnings import check_warnings
from chatbot import chatbot_response
from pdf_report import create_pdf_report


load_dotenv()

app = FastAPI()

create_database()


@app.get("/")
def home():

    return {
        "message": "MediGrid AI API is running"
    }


@app.post("/read_prescription")
async def read_prescription_endpoint(
    file: UploadFile = File(...)
):

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        return {
            "error": "GEMINI_API_KEY not found"
        }

    content = await file.read()

    image = io.BytesIO(content)

    try:

        return read_prescription(
            image,
            api_key
        )

    except Exception as e:

        return {
            "error": str(e)
        }


@app.post("/save_prescription")
def save_prescription_endpoint(
    data: dict
):

    save_prescription(data)

    return {
        "status": "saved"
    }


@app.get("/get_prescriptions")
def get_prescriptions_endpoint():

    return get_prescriptions()


@app.get("/get_location")
def get_location_endpoint():

    return get_location()


@app.get("/find_pharmacies")
def find_pharmacies_endpoint():

    return find_pharmacies()


@app.post("/check_warnings")
def check_warnings_endpoint(
    data: dict
):

    return check_warnings(
        data.get("medicines", [])
    )


@app.post("/chat")
def chat_endpoint(
    message: str
):

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    return {
        "response": chatbot_response(
            message,
            api_key
        )
    }


@app.post("/pdf_report")
def pdf_report_endpoint(
    data: dict
):

    filename = create_pdf_report(data)

    return {
        "status": "success",
        "file": filename
    }