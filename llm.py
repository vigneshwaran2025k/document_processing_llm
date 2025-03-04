import json
import os
from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

def text_to_json_usingllm(prompt, model="llama-3.3-70b-versatile"):
    """
    Generates a response from the Groq API based on the given prompt and converts it to JSON format.
    
    Parameters:
    prompt (str): The prompt to send to the model.
    model (str): The model to use for generation.
    
    Returns:
    dict: The generated response from the model in JSON format.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in the environment variables")
    
    client = Groq(api_key=api_key)
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert in data extraction. Your task is to analyze text input and provide structured JSON output with key-value pairs, extracting important details accurately."},
            {"role": "user", "content": prompt}
        ],
        model=model,
        stream=False,
    )
    
    response_text = chat_completion.choices[0].message.content
    
    try:
        response_json = json.loads(response_text)
    except json.JSONDecodeError:
        response_json = {"response": response_text}
    
    return response_json

