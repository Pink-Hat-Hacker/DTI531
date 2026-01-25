# ai
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("LITELLM_TOKEN")
llm_client = OpenAI(api_key=token, base_url="https://litellm.oit.duke.edu/v1")

payload = {
            "Room": f"Wilk 127",
            "temperature": 32,
            "humidity": 45,
            "timestamp": 1/24/2026
        }

prompt = (
    "You are a plant expert. Analyze the following sensor data and recommend which types of plants would thrive in this room. Limit your response to exactly 3 sentences.\n\n"
    f"Sensor data:\n{payload}"
)

try:
    response = llm_client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    analysis = response.output_text
    print("\nPlant Analysis:")
    print(analysis)

except Exception as e:
    print(f"Error calling LLM: {e}")