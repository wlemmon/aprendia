'''

{
"title": "I like cats",
"source_locale": "en_us",
"target_locale": "es_co",
"language_level": "A1",
"age_level": "2",
"topic": "running arrands",
"conversation_type": "narrating activities to help toddler acquire language",
"min_sentence_length": 3,
"max_sentence_length": 10
}
'''
pip install google-generativeai


model = GenerativeModel("gemini-2.5-pro-vision") # Use vision model for images

# Assuming you have an image accessible via a URI (e.g., in Cloud Storage)
image_uri = "gs://your-bucket/your-image.jpg" 

prompt_parts = [
    Part.from_text("Describe this image and identify any objects present."),
    Part.from_uri(image_uri, mime_type="image/jpeg"),
]

response = model.generate_content(prompt_parts)
print(response.candidates[0].content.parts[0].text)