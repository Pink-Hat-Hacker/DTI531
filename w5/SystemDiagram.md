# Project Description
This project identifoes the type of plastic material (PET, PE, PVC, etc.) based on "sensor data" and determines the appropriate sorting category. Since the midterm does not require hardware, the "sensor" data will be static inputs that are entered into a specific schema. The simulated data will then be sent to an API which will then output the appropriate category. *Potential changes includes: focusing on trash identification via a camera (depending on sensor prices for plastic identification). The process would be similar, utilitizing the camera, computer vision, and an API to determine the type of material being categorized.*

# System Diagram
![system](system.drawio.png)

## System Functionality
1. "Sensor Data" Input
*Data input will either be static to simulate sensor data or will be data from the computer webcam. Distiguishment made because this will either be a plastic identification project or a trash sorting project. Depends on the sensor availability and feasibility within budget constraints.*
**Sensor for Plastic Identification**
- Provides static material property data
- Example inputs:
    - Spectral signature values
    - Density
    - Reflectance
**Camera for trash identification**
- Provides an image capture of the trash "seen" via the webcam
- Example inputs:
    - captured image
    - computer vision shape capture
    - utlization of this git repo: https://github.com/garythung/trashnet

2. API Layer 1
- Receives a data via POST request
- Validation of information (proper schema and needed data for identification), if not error message is returned ("Scan again!")
- Routes the data to the processing layer

3. Data Validation Layer
- Happens within the API Layer
- Ensures:
    - Required fields exist
    - Values are within acceptable ranges
    - Correct data types
    - Rejects improper requests

4. Data Processing Layer
- Normalizes sensor data (any numbers that need to be rounded or converted)
    - If an image for computer vision, any layers of edits that need to be applied for proper classification (contrast, removal of background, etc.)
- Extracts relevant classification features
- Transforms raw values into model-ready input (proper schema)

5. Classification
- Uses:
    - Rule-based logic or Pre-trained ML model, AI LLM RAG system, etc.
- Outputs:
    - Plastic type (e.g., PET, HDPE) or Waste type
    - Confidence score

6. Sorting Category Decision
-  Mapping output to sorting category (this would be an MQTT layer for the stepper motor to move the waste into the correct place)

7. Response
- Sends data to user about categorization, confidence, and prompts for input of correctness

8. Data Storage
All inputs and outputs are stored into a dynamic database that can be validated by system owner (potentially for the RAG model)

## Data Flow
```
[Simulated Sensor Data]
          │
          ▼
[API Gateway] ––▶ [Validation Layer]
          │
          ▼
[Data Processing]
          │ (data transformed)
          ▼
[Classification Engine]
          │ (prediction generated)
          ▼
[Sorting Decision Module]
          │
          ▼
[Response Output]
          │
          ▼
[Database Storage]
```
## Pseudocode Implementation

### Raw sensor data
```
{
  "spectral_signature": [0.21, 0.45, 0.78],
  "density": 1.38,
  "reflectance": 0.62
}
```
### OpenCV - Computer Vision with classification
```
{
  "frame_id": 1827,
  "camera_id": 0,
  "resolution": {
    "width": 1280,
    "height": 720
  },
  "detections": [
    {
      "object_id": 1,
      "label": "plastic_bottle",
      "material_type": "PET",
      "confidence": 0.94,
      "bounding_box": {
        "width": 165,
        "height": 342
      },
      "sorting_category": "Category_A"
    },
    {
      "object_id": 2,
      "label": "aluminum_can",
      "material_type": "Aluminum",
      "confidence": 0.89,
      "bounding_box": {
        "width": 120,
        "height": 210
      },
      "sorting_category": "Category_B"
    }
  ],
  "processing_time_ms": 27,
  "status": "success"
}
```
### Classification Response
```
{
  "material_type": "PET",
  "confidence": 0.94,
  "sorting_category": "Category_A",
  "status": "success"
}
```
### AI LLM Response for Readability
"*`The material was identified as PET with 94% confidence, successfully classified into Category_A.`*"

### Classification Logic
``` 
classify_material(processed_data):

    INPUT: processed_data

    model = initialize_classification_engine()

    prediction = model.predict(processed_data)

    plastic_type = prediction.label
    confidence = prediction.probability

    IF confidence < confidence_threshold:
        plastic_type = "UNKNOWN"

    RETURN {
        "plastic_type": plastic_type,
        "confidence": confidence
    }
```