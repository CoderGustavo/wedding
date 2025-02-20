from starlette.exceptions import HTTPException
import os
from fastapi.responses import JSONResponse
import base64
from random import randint
#import g4f
import json

from utilities.Logger import logger

import google.generativeai as genai
import os

import re
import html

from bson import ObjectId

class Reusable():
    # Reusable class
    # methods of this class are:
    # ['__init__', 'throw_error', 'random_number', 'use_ai', 'sanitize_input]

    def __init__(self):
        pass

    def throw_error(self, fieldName, error, exception=True):
        errorMessage = error.get('msg').replace('<<field>>', f"'{fieldName}'");
        if exception:
            raise HTTPException(status_code=error.get('status_code'), detail=errorMessage)
        else:
            return JSONResponse(content=errorMessage, status_code=error.get('status_code'))

    def random_number(self):
        return randint(999, 9999)

    def use_ai(self, model, message):
        genai.configure(api_key=os.environ["GEMINI_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(message)

        return json.loads(response.text.replace("```json", "").replace("```", ""))

    def convert_objectid_to_str(self, doc):
        """
        Convert ObjectId fields in a MongoDB document to string.
        Recursively handles nested dictionaries and lists.
        """
        if isinstance(doc, dict):
            return {(k if k != "_id" else "id"): str(v) if isinstance(v, ObjectId) else self.convert_objectid_to_str(v) for k, v in doc.items()}
        elif isinstance(doc, list):
            return [self.convert_objectid_to_str(i) for i in doc]
        else:
            return doc

    def sanitize_input(self, value):
        """
        Sanitize input to prevent SQL injection attacks and other injection attacks.
        This function ensures that inputs are clean for use in SQL statements and protects
        against SQL injection by escaping harmful characters and validating expected data types.
        """
     
        # Handle string inputs
        if isinstance(value, str):
            # Escape single quotes and backslashes
            value = value.replace("'", "''").replace("\\", "\\\\")
         
            # Remove semicolons and double hyphens, common in SQL injection
            value = re.sub(r"[;]", "", value)
            value = re.sub(r"--", "", value)

            # Encode HTML to handle any XSS concerns for front-end usage
            value = html.escape(value)

            # Validate string length (optional, based on your needs)
            if len(value) > 1000:
                raise ValueError("Input value exceeds maximum allowed length.")

            return value

        # Handle integer and numeric values
        elif isinstance(value, int) or isinstance(value, float):
            # Ensure the value is indeed numeric and within expected range
            if not (isinstance(value, int) or isinstance(value, float)):
                raise ValueError("Numeric value is not of a valid type.")
            return value  # Numeric types are safe to pass directly as long as they're validated

        # Handle booleans
        elif isinstance(value, bool):
            return value

        # Handle other types (lists, dictionaries) carefully, if needed
        elif isinstance(value, list):
            return [self.sanitize_input(v) for v in value]  # Recursively sanitize lists

        elif isinstance(value, dict):
            return {k: self.sanitize_input(v) for k, v in value.items()}  # Recursively sanitize dicts

        else:
            # Raise an error for unsupported types
            raise ValueError(f"Unsupported input type: {type(value)}")


    def format_phone_number(self, value: str) -> str:
        try:
            phone = ''.join(filter(str.isdigit, value))
            fix_phone = str(int(phone))
        except Exception:
            raise ValueError("Número de telefone inválido. Use o formato (XX) 9XXXX-XXXX.")
        if len(fix_phone) == 10 and value.startswith("0"):
            fix_phone = f"0{fix_phone}"
        if len(fix_phone) == 11:  # Número com DDD e 9º dígito (ex: 11987654321)
            return f'({fix_phone[:2]}) {fix_phone[2:7]}-{fix_phone[7:]}'
        else:
            raise ValueError("Número de telefone inválido. Use o formato (XX) 9XXXX-XXXX.")


