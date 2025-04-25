import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key
genai.configure(api_key="api_key")

generation_config={
    "temperature":0.4,
    "top_p" :1,
    "top_k":32,
    "max_output_tokens":4096,
}

# apply safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]
system_prompt="""
You are given medical images such as photos of skin patches, stomach ulcers, or visible injuries. 
The task is to carefully examine each image and detect any abnormality, irregularity, or visible sign of disease. 
Look for anything unusual compared to healthy tissue, such as changes in color, texture, shape, size, or the presence of wounds, swelling, ulcers, spots, or lesions.
 Once an anomaly is detected, mark it clearly and provide a detailed explanation describing what has been found. 
 The explanation should include observations like the type of abnormality, its possible cause, how severe it looks, 
 and whether it could indicate a minor condition or something more serious. 
 The results should help a medical professional by giving a clear description of what is abnormal, where it is located, and why it may require attention.
 If the image quality is not good enough to compute analysis, don't make assumptions, communicate it to the user.
 Also, provide a caution that this could be wrong. consult a doctor for more clear analysis.
 """
#model config
model=genai.GenerativeModel(model_name="gemini",
                            generation_config=generation_config,
                            safety_settings=safety_settings)


st.set_page_config(page_title='Vital Image analytics', page_icon=':robot:')
st.image("C:/Users/Mathi/Desktop/Medical Image Detection App/logo.png", width=100)
st.title("Vital Image Analysis")
st.subheader("For Identifying and analyzing medical images")
uploaded_file=st.file_uploader("Upload the medical image", type=['jpg','png', 'jpeg'])
if uploaded_file:
    image_data=uploaded_file.getvalue()
    st.image(image_data, width=500)
submit_button=st.button("Generate the analysis")

if submit_button:
    image_parts=[
        {
            "mime_type": "image/jpeg",
            "data":image_data
        }
    ]
    prompt_parts=[
        image_parts[0],
        system_prompt,
    ]
    #generating response
    
    response=model.generate_content(prompt_parts)
    st.write(response.text)

 
