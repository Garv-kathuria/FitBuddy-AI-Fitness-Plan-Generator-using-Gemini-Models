import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_ID = "gemini-2.5-flash"

def generate_nutrition_tip_with_flash(goal):
    """Generates a single, highly specific nutrition tip based on the goal."""
    prompt = f"""
    You are an expert sports nutritionist. Give me ONE short, highly actionable nutrition tip 
    (maximum 2 sentences) specifically for someone whose main fitness goal is: {goal}.
    """
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    return response.text
