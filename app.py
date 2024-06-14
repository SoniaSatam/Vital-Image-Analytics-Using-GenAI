import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configuration for the generative AI model
genai.configure(api_key=api_key)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }
)

system_prompt = """
As a highly skilled medical practitioner specialising in image analysis you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the image.

Your Responsibilities include:
1. Detailed Analysis: Thoroughly analyse each image focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggests potential next steps, including further test or treatment as applicable.
4. Treatment Suggestions: If appropriate recommend possible treatment options or interventions.

Important Notes:
1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impaired clear analysis note that certain aspects are 'Unable to be determined based on the provided image'.
3. Disclaimer: Accompany or analysis with the disclaimer: "Consult with a doctor before making any decisions."
4. Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis adhering to the structured approach outlined above.

Please provide me output response with these 4 headings: Detailed Analysis, Findings Report, Recommendations and Next Steps, Treatment Suggestions
"""

# Setting the page configuration
st.set_page_config(page_title="Vital Image Analytics📊", page_icon="🤖")

# Custom CSS for background color and other styling
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
            color: #333;
        }
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;  /* Dark Blue Color */
        }
        footer {
            font-size: 0.8rem;
            color: #888;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Main title and subtitle
st.markdown("<h1 style='text-align: center;'>Vital Image Analytics📊</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #808080;'>An application to help users identify medical images</h3>", unsafe_allow_html=True)

# Instructions
st.markdown("### Instructions:")
st.markdown("1. Upload a medical image in PNG, JPG, or JPEG format.")
st.markdown("2. Click on 'Generate the Analysis' to get the detailed report.")
st.markdown("3. The report will include Detailed Analysis, Findings Report, Recommendations, and Treatment Suggestions.")

# Upload file
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])

# Display the uploaded image
if uploaded_file:
    st.image(uploaded_file, width=300, caption="Uploaded Medical Image")

# Generate Analysis button
submit_button = st.button("Generate the Analysis")

if submit_button and uploaded_file is not None:
    # Show a spinner while processing
    with st.spinner('Analyzing the image...'):
        image_data = uploaded_file.getvalue()
        prompt_parts = [
            {"mime_type": "image/jpeg", "data": image_data},
            {"text": system_prompt},
        ]
        
        response = model.generate_content({"parts": prompt_parts})

    # Display the analysis result
    st.markdown("<h2>Here is the analysis based on your image:</h2>", unsafe_allow_html=True)
    st.write(response.text)

# Footer
st.markdown("---")
st.markdown("<footer style='text-align: center;'>Vital Image Analytics - Powered by Generative AI</footer>", unsafe_allow_html=True)
