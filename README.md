# APIFern - AI Chatbot with API Integration

APIFern is an intelligent AI-powered chatbot that can process user queries, decide whether to answer directly, use external tools, or call APIs based on a Swagger-based API definition. It leverages the Mistral model via Ollama for natural language processing.

## Features
- **Natural Language Understanding**: Uses `mistral` to understand and respond to user queries.
- **API Integration**: Calls APIs dynamically based on a provided Swagger file.
- **Tool Execution**: Integrates with external tools for additional functionality.
- **Human-Readable Responses**: Transforms API responses into clear, concise language.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- `ollama` for model execution
- Required Python libraries (install using the command below)

```bash
pip install requests json
```

## Usage
1. **Prepare the API Schema**: Place your Swagger JSON file in `static/swagger.json`.
2. **Run the chatbot**:
   ```bash
   python chatbot.py
   ```
3. **Chat with the assistant**: The chatbot will decide whether to answer directly, use a tool, or call an API.

## How It Works
1. Loads the `swagger.json` file to extract available APIs.
2. Uses a structured system prompt to instruct `mistral` on how to respond.
3. Determines the best action:
   - Direct response
   - Using an external tool
   - Calling an API
4. Calls APIs dynamically, formats responses, and presents them in human-readable language.

## Example Interaction
```
👤 You: What's the weather today?
🤖 I can fetch weather data. Calling the weather API...
🤖 It's currently 22°C with clear skies.
```

## API Handling
- The chatbot extracts API details from `swagger.json`.
- Calls APIs dynamically with proper parameters.
- Handles GET, POST, and DELETE requests.
- Returns a structured error message in case of failures.

## Customization
- Modify `TOOLS` in `chatbot_tools.py` to add custom tools.
- Update `SYSTEM_PROMPT` for different chatbot behavior.

## Exit
To exit the chatbot, type `exit`.

## License
This project is licensed under the MIT License.
