import ollama
import requests
import json
from chatbot_tools import TOOLS

# Load the Swagger file
with open("static/swagger.json", "r") as f:
    SWAGGER_JSON = json.load(f)

# Extract available APIs from the Swagger file
AVAILABLE_APIS = [
    {
        "name": path.split("/")[-1],
        "method": method.upper(),
        "path": path,
        "parameters": [
            {
                "name": param["name"],
                "in": param["in"],
                "description": param.get("description", ""),
                "required": param.get("required", False),
                "type": param["schema"]["type"] if "schema" in param and "type" in param["schema"] else "string"
            }
            for param in details.get("parameters", [])
        ]
    }
    for path, methods in SWAGGER_JSON["paths"].items()
    for method, details in methods.items()
]

# Update the SYSTEM_PROMPT
SYSTEM_PROMPT = f"""
You are an AI assistant with access to specialized tools.
When the user makes a request, decide whether to:
1. Respond directly
2. Use an external tool

Respond in the following format:
{{"action": "tool_name", "query": "text to pass to the tool"}}
or
{{"action": "chat", "response": "normal response"}}
or
{{"action": "api", "query": {{"name": "api_name", "params": {{"parameter1": "value1", "parameter2": "value2"}}}}}}

The available APIs are:
{json.dumps(AVAILABLE_APIS, indent=2)}

For each API, the required parameters are specified. If you choose to use an API, include all required parameters in the "params" field.
If the request does not require a tool or an API, respond directly.
"""

def call_api(api_name, query_params=None):
    """
    Makes an API call to localhost:5000 using the specified API name.
    """
    try:
        # Find the API in the Swagger JSON
        api = next((api for api in AVAILABLE_APIS if api["name"] == api_name), None)
        if not api:
            return f"⚠️ API '{api_name}' not found."

        # Build the URL
        url = f"http://localhost:5000{api['path']}"
        if query_params:
            url = url.format(**query_params)

        # Make the HTTP request
        if api["method"] == "GET":
            response = requests.get(url, params=query_params)
        elif api["method"] == "POST":
            response = requests.post(url, json=query_params)
        elif api["method"] == "DELETE":
            response = requests.delete(url, params=query_params)
        else:
            return f"⚠️ HTTP method '{api['method']}' not supported."

        # Return the result
        if response.status_code == 200:
            return response.json()
        else:
            return f"⚠️ API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"⚠️ Error during API call: {e}"

def process_request(user_input):
    """Uses Ollama to decide whether to use a tool or respond normally."""
    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ]
    )

    try:
        result = json.loads(response["message"]["content"])
        
        if result["action"] == "chat":
            return result["response"]
        elif result["action"] in TOOLS:  # Check if the tool exists
            return TOOLS[result["action"]](result["query"])
        elif result["action"] == "api":  # New action to call an API
            api_response = call_api(result["query"]["name"], result["query"].get("params", {}))
            
            # Pass the API response and user query to the model to generate a human-readable response
            return generate_human_readable_response(user_input, api_response)
        else:
            return "⚠️ Unrecognized action."
    except json.JSONDecodeError:
        return "⚠️ Error in response format."
    except KeyError as e:
        return f"⚠️ Missing field in response: {e}"
    except Exception as e:
        return f"⚠️ Error processing response: {e}"

def generate_human_readable_response(user_input, api_response):
    print(f"API Response: {api_response}")
    print(f"User Input: {user_input}")
    """
    Uses the model to generate a human-readable response
    based on the user's query and the API response.
    """
    prompt = f"""
You are an AI assistant. Your task is to provide a human-readable answer to the user by accurately interpreting the API response.

### User Question:
"{user_input}"

### API Response (JSON):
{json.dumps(api_response, indent=2)}

### Instructions:
- Base your response ONLY on the API response. Do NOT invent or assume any information.
- If the API response contains an error or missing data, inform the user clearly.
- Summarize the API response in a natural, easy-to-understand way.
- If relevant, include key details but avoid excessive repetition.

Now, generate the response:
"""

    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    try:
        return response["message"]["content"]
    except KeyError:
        return "⚠️ Error generating the response."
    
def chat_with_ollama():
    print("🤖 Intelligent Chatbot with Tools - Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("👤 You: ")
            if user_input.lower() == "exit":
                print("👋 Goodbye!")
                break

            response = process_request(user_input)
            print(f"🤖 {response}\n")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    chat_with_ollama()