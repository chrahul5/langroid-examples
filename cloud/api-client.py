"""
This file defines a simple langroid API python client.
"""
import requests

class LangroidAgent:
    def __init__(self):
        self.api_url = "http://127.0.0.1:8080/langroid/agent/completions"

    def llm_response(self, prompt):
        # Usage of the client function
        data_payload = {
            "prompt": prompt
        }

        # Make the POST request with the requests library
        try:
            response = requests.post(self.api_url, json=data_payload)

            # Check the response status code
            if response.status_code == 200:  # Replace with the appropriate status code for success
                # You can access the response content or JSON data if applicable
                response_data = response.json()
                return response_data
            else:
                return {"status_code": response.status_code, "message": "POST request failed"}
                
        except requests.exceptions.RequestException as e:
            return { "message": f"Got exception {e}"}

# Example usage.
lr_agent = LangroidAgent()
print(lr_agent.llm_response("What is capital of US?"))