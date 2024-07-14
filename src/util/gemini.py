import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

api_key=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)
safety_settings = [
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]

model = genai.GenerativeModel(
  model_name='gemini-1.5-flash-latest',
  safety_settings=safety_settings,
)