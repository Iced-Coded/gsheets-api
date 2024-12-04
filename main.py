from typing import Union
import os
import json
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import gspread
from google.oauth2.service_account import Credentials
import uvicorn  # Required to run the app programmatically

# Retrieve the JSON string from the environment variable
service_account_json = os.environ["GOOGLE_SERVICE_ACCOUNT"]

# Parse the JSON string into a Python dictionary
service_account_info = json.loads(service_account_json)

# Create credentials directly from the dictionary
credentials = Credentials.from_service_account_info(
    service_account_info,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)

# Authenticate with gspread
gc = gspread.authorize(credentials)
spreadsheet = gc.open("POLITIME Донат")
worksheet = spreadsheet.sheet1

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/prices")
def read_prices():
    # Fetch range E2:G8
    data = worksheet.get("E2:G8")  # Adjust range as needed

    # Process data into the desired format
    processed_data = {}
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            key = f"{row_index}_{col_index + 1}"  # Adjust for desired format
            processed_data[key] = value

    return processed_data

# Main entry point
if __name__ == "__main__":
    # Get the port from the environment variable (Render.com sets this automatically)
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)
