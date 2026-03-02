import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_ID = "gemini-2.5-flash" 

def generate_workout_gemini(name, age, weight, goal, intensity):
    """Generates a 7-day workout plan using Gemini."""
    prompt = f"""
    You are an expert personal trainer. Create a 7-day workout plan for:
    Name: {name}
    Age: {age}
    Weight: {weight}kg
    Goal: {goal}
    Intensity: {intensity}

    Format the response in clean Markdown. Include a mix of exercises, sets, reps, and rest days.
    """
    
    # The new syntax for calling the model
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    return response.text
