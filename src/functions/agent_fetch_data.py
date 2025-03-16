import requests
import logging

logger = logging.getLogger(__name__)
def agent_fetch_data(api_query: str) -> str:
    """
    Uses RAG to find the correct API, retrieves the necessary parameters, and makes a request.
    """

    try:    
        # Normalize method to uppercase
        method = api_query["method"].upper()
        endpoint = api_query["endpoint"]
        params = api_query.get("params", {})

        logger.info(f"Calling API: {method} {endpoint} with params: {params}")
    
        # Dispatch the correct HTTP request
        response = None
        if method == "GET":
            response = requests.get(endpoint, params=params, verify=False)
        elif method == "POST":
            response = requests.post(endpoint, json=params, verify=False)
        elif method == "PUT":
            response = requests.put(endpoint, json=params, verify=False)
        elif method == "DELETE":
            response = requests.delete(endpoint, json=params, verify=False)
        else:
            logger.error(f"Unsupported HTTP method: {method}")
            return f"Error: HTTP method '{method}' not supported."

        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error calling API: {e}")
        return "Error fetching data."