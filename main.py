from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image, UnidentifiedImageError
import pytesseract
import pandas as pd
import os
import fitz
from io import BytesIO
from llm import text_to_json_usingllm
from json_identifier import extract_json_from_response
app = FastAPI()

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    try:
        file_extension = os.path.splitext(file.filename)[-1].lower()
        print(f"File Name: {file.filename}, MIME Type: {file.content_type}, Extension: {file_extension}")

        # Handle CSV and XLSX files
        if file_extension == ".csv" or file.content_type == "text/csv":
            df = pd.read_csv(file.file)
            structured_data = df.to_dict(orient="records")  # Properly convert to JSON
            return {"filename": file.filename, "structured_data": structured_data}

        elif file_extension == ".xlsx" or file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(file.file, engine="openpyxl")
            structured_data = df.to_dict(orient="records")  # Properly convert to JSON

            return {"filename": file.filename, "structured_data": structured_data}
        
        # Handle PDF files
        elif file_extension == ".pdf" or file.content_type == "application/pdf":
            pdf_data = await file.read()
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            
            extracted_text = ""
            for page in doc:
                extracted_text += page.get_text() + "\n"

            if not extracted_text.strip():
                raise HTTPException(status_code=404, detail="No text detected in the PDF")
            prompt = f"""
                        Analyze the following text and extract key details in a well-structured JSON format. Identify important entities such as names, dates, IDs, monetary values, addresses, product details, and any other relevant information.

                        **Instructions:**
                        - Ensure the JSON output follows a structured format with clear key-value pairs.
                        - Convert numerical values to appropriate data types (e.g., integers, floats, dates).
                        - Identify and categorize entities properly (e.g., "Invoice Number", "Customer Name", "Amount", "Date").
                        - If certain data appears in a tabular format, structure it as an array of objects.
                        - Do not add extra information or assumptions outside the given text.

                        **Text to Process:**
                        {extracted_text}
                        """
            print("extracted text",extracted_text)

            # prompt = f"Extract key details from the following text and return a structured JSON format:\n\n{extracted_text}"


            raw_response = text_to_json_usingllm(prompt)
            structured_data = extract_json_from_response(raw_response.get("response", ""))

            return {"filename": file.filename, "structured_data": structured_data}


        # Ensure file is an image before processing with OCR
        elif file_extension in [".jpg", ".jpeg", ".png"] or file.content_type in ["image/jpeg", "image/png"]:
            image_data = await file.read()
            try:
                image = Image.open(BytesIO(image_data))
            except UnidentifiedImageError:
                raise HTTPException(status_code=400, detail="Invalid or corrupt image file")
            extracted_text = pytesseract.image_to_string(image).strip()
            cleaned_text = " ".join(extracted_text.split())

            if not cleaned_text:
                raise HTTPException(status_code=404, detail="No text detected in the image")
            # prompt = f"Extract key details from the following text and return a structured JSON format:\n\n{cleaned_text}"
            prompt = f"""
                        Analyze the following text and extract key details in a well-structured JSON format. Identify important entities such as names, dates, IDs, monetary values, addresses, product details, and any other relevant information.

                        **Instructions:**
                        - Ensure the JSON output follows a structured format with clear key-value pairs.
                        - Convert numerical values to appropriate data types (e.g., integers, floats, dates).
                        - Identify and categorize entities properly (e.g., "Invoice Number", "Customer Name", "Amount", "Date").
                        - If certain data appears in a tabular format, structure it as an array of objects.
                        - Do not add extra information or assumptions outside the given text.

                        **Text to Process:**
                        {cleaned_text}
                        """
            
            print("cleaned_text ",cleaned_text)
            raw_response = text_to_json_usingllm(prompt)
            structured_data = extract_json_from_response(raw_response.get("response", ""))
            return {"filename": file.filename, "structured_data": structured_data}
        else:
            raise HTTPException(status_code=400, detail="Only JPG, PNG, CSV, and XLSX files are supported")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
