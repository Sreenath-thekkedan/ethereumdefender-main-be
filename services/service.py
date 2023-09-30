import requests
import joblib
from http import HTTPStatus
import re
from datetime import datetime
import pandas as pd
from models.exceptions import BlockNotFoundException
from requests.exceptions import RequestException

import logging

# Configure the logging settings
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger
logger = logging.getLogger(__name__)


BLOCK_DETAILS_URL_BASE = "https://api.blockcypher.com/v1/eth/main/txs/"
def fetch_block_details(hash: str):
    api_url = BLOCK_DETAILS_URL_BASE + hash

    
    response = requests.get(api_url)
    if response.status_code == HTTPStatus.OK:
        block_details = response.json()
        return block_details
    elif response.status_code == HTTPStatus.NOT_FOUND:
        raise BlockNotFoundException
    else:
        return {"error": f"API request to fetch block failed with status code {response.status_code}."}
    

def load_and_predict(input_data, model_filename="./data/svm_model.joblib"):
    """
    Load a trained SVM model and make predictions on input data.

    Args:
        input_data (array-like): New data for prediction.
        model_filename (str): Filename of the trained SVM model (default is "svm_model.joblib").

    Returns:
        list: Predicted labels for the input data.
    """
    # List of feature names
    feature_names = [
        "block_height",
        "block_index",
        "total",
        "fees",
        "size",
        "gas_limit",
        "gas_used",
        "gas_price",
        "gas_tip_cap",
        "gas_fee_cap",
        "confirmed",
        "received",
        "ver",
        "double_spend",
        "vin_sz",
        "vout_sz",
        "confirmations",
        "confidence"
    ]

    try:
        # Load the trained SVM model from the specified file
        loaded_model = joblib.load(model_filename)
        
        # Make predictions on the input data
        # Convert the list into a DataFrame with feature names as columns
        input_data_df = pd.DataFrame([input_data], columns=feature_names)
        
        predictions = loaded_model.predict(input_data_df)
        
        if predictions[0] == 0:
            return False
        else:
            return True
    except Exception as e:
        return str(e)

def convert_time_to_float(time_string):
    # Remove the 'T' and 'Z' characters from the time string
    time_string = time_string.replace('T', ' ').replace('Z', '')

    format_strings = ['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S']

    for format_string in format_strings:
        try:
            # Convert the time string to a datetime object
            datetime_obj = datetime.strptime(time_string, format_string)

            # Convert the datetime object to a float value
            float_value = datetime_obj.timestamp()

            return float_value
        except ValueError:
            pass

    # If no match is found, return None
    #return None

    # Convert the datetime object to a float value
    float_value = datetime_obj.timestamp()

    return float_value

def prepare_input_data(block_details):
    # Extract relevant keys from block details
    relevant_keys = [
        "block_height",
        "block_index",
        "total",
        "fees",
        "size",
        "gas_limit",
        "gas_used",
        "gas_price",
        "gas_tip_cap",
        "gas_fee_cap",
        "confirmed",
        "received",
        "ver",
        "double_spend",
        "vin_sz",
        "vout_sz",
        "confirmations"
    ]

    # Create a dictionary to hold the input data
    input_data = {}

    # Iterate through the relevant keys and add them to the input data dictionary
    for key in relevant_keys:
        input_data[key] = block_details.get(key, None)

    # Convert the "received" time string to a float using the convert_time_to_float function
    input_data["received"] = convert_time_to_float(input_data["received"])
    input_data["confirmed"] = convert_time_to_float(input_data["confirmed"])

    # Add the "confidence" feature with a constant value of 1
    input_data["confidence"] = 1

    # Organize the data in the desired order
    input_data_ordered = [
        input_data["block_height"],
        input_data["block_index"],
        input_data["total"],
        input_data["fees"],
        input_data["size"],
        input_data["gas_limit"],
        input_data["gas_used"],
        input_data["gas_price"],
        input_data["gas_tip_cap"],
        input_data["gas_fee_cap"],
        input_data["confirmed"],
        input_data["received"],
        input_data["ver"],
        input_data["double_spend"],
        input_data["vin_sz"],
        input_data["vout_sz"],
        input_data["confirmations"],
        input_data["confidence"]
    ]

    return input_data_ordered

def verify_block(hash: str) -> bool:
    try:
        block_details = fetch_block_details(hash)
        input_data = prepare_input_data(block_details)
        return load_and_predict(input_data)
    except BlockNotFoundException:
        logger.error('Block not found')
        raise BlockNotFoundException
    except RequestException as e:
        logger.error("Cannot connect to network")
        raise RequestException
    except Exception as e:
       logger.error('Error occurred ' + str(e))