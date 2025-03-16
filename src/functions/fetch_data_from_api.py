import requests

def fetch_data_from_api(api_name: str, params: dict) -> str:
    """
    Calls the appropriate API with the correct parameters.
    """
    if api_name not in API_CATALOG:
        return "API not found."

    api_info = API_CATALOG[api_name]
    try:
        if api_info["method"] == "GET":
            response = requests.get(api_info["endpoint"], params=params)
        else:
            response = requests.post(api_info["endpoint"], json=params)
        
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error accessing API {api_name}: {e}")
        return "Error fetching data."