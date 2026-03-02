import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_ID = "gemini-2.5-flash"

def update_workout_plan(current_plan, feedback):
    """Modifies an existing plan based on user feedback."""
    prompt = f"""
    You are an expert personal trainer. 
    Here is the client's current workout plan:
    {current_plan}

    The client has provided the following feedback/request for changes:
    "{feedback}"

    Please rewrite the entire 7-day workout plan incorporating their feedback. 
    Keep the formatting in clean Markdown.
    """
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    return response.text
