import json

def extract_json_from_response(llm_response):
    try:
        start_index = llm_response.find("```json")
        end_index = llm_response.rfind("```")

        if start_index != -1 and end_index != -1:
            json_text = llm_response[start_index + 7:end_index].strip()
            return json.loads(json_text)
        else:
            return {"error": "No valid JSON structure found in response"}
    
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in response"}