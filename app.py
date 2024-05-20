from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="BioDetect", page_icon=":sparkles:")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Select a page:", ["Home", "Upload Image"])

if page == "Home":
    # Home page content
    st.title("Welcome to BioDetect Health App")
    st.image("C:\\Users\\smart\\Downloads\\genai\\doct.jpeg", use_column_width=True)
    st.markdown("""
    ## What is BioDetect App?
    BioDetect Health App leverages advanced AI technology to analyze hair and body images to diagnose potential issues. Whether it's hair thinning, skin conditions, or other dermatological concerns, our app provides insights, recommended treatments, and preventative measures.
    In the field of dermatology and trichology, accurately diagnosing hair and skin conditions can be challenging due to the wide range of potential issues and their varying symptoms. Patients often face delays in receiving appropriate treatments due to the need for specialist consultations and comprehensive examinations. There is a pressing need for a technological solution that can quickly and accurately identify hair and skin problems from images, providing immediate diagnostic feedback and treatment recommendations.
    ### Features:
    - **Quick Diagnostics**: Upload your hair or body images and get immediate analysis.
    - **Expert Recommendations**: Receive personalized treatment plans and precautions.
    - **Comprehensive Insights**: Understand the health of your hair and skin with detailed reports.
    
    ### How to Use:
    1. Navigate to the "Upload Image" section.
    2. Provide an input prompt describing your concern.
    3. Upload an image for analysis.
    4. Receive diagnostic results and recommendations instantly.
    
    Get started by navigating to the "Upload Image" section!
    """)
elif page == "Upload Image":
      st.header("Upload Image for Analysis")
      input=st.text_input("Input Prompt: ",key="input")
      uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
      image=""   
      if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)


        submit=st.button("check the condition")

        input_prompt="""
        You are an expert in hair specialist and dermitologist where you need to see the hair and body images of the person  from the image
               and find out the problem that person facing , also provide the medicines and  precautions details of every diseases
                in the image


        """

## If submit button is clicked

        if submit:
          image_data=input_image_setup(uploaded_file)
          response=get_gemini_repsonse(input_prompt,image_data,input)
          st.subheader("The Response is")
          st.write(response)

# Custom CSS for styling
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(90deg, rgba(135,182,194,1) 0%, rgba(255,252,217,1) 100%);
        color: #000;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, rgba(135,182,194,1) 0%, rgba(255,252,217,1) 100%);
    }
    .stButton>button {
        color: white;
        background-color: #007bff;
        border-radius: 8px;
    }
    .stTextInput>div>input {
        border-radius: 8px;
        border: 2px solid #007bff;
    }
    .stFileUploader>label>div {
        border-radius: 8px;
        border: 2px solid #007bff;
    }
</style>
""", unsafe_allow_html=True)