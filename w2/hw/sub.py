# subscriber.py
import paho.mqtt.client as mqtt
import time
# ai
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("LITELLM_TOKEN")
llm_client = OpenAI(api_key=token, base_url="https://litellm.oit.duke.edu/v1")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker")
        # Subscribe to topic
        client.subscribe("pythontest/sensors/mysensor")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    # modification 2)
    payload = msg.payload.decode()
    print(f"Received message on topic {msg.topic}: {payload}")

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

# Create subscriber client
subscriber = mqtt.Client()
subscriber.on_connect = on_connect
subscriber.on_message = on_message

# Connect to public broker
print("Connecting to broker...")
subscriber.connect("test.mosquitto.org", 1883, 60)

# Start the subscriber loop
subscriber.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping subscriber...")
    subscriber.loop_stop()
    subscriber.disconnect()