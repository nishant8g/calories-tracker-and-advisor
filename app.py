import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input_prompt,image[0]])
    return response.text


def input_image_setup(uploaded_file):
    #read if a file is uploaded
    if uploaded_file is not None:
        #read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    
## initialize our streamlit app frontend setup
st.set_page_config(page_title="Calories Advisor App")
st.header("Calories Advisor App")
uploaded_file=st.file_uploader("Choose an image...",type=['Jpg','jpeg','Png'])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image.",use_column_width=True)

submit=st.button("Tell me about the total calories")

input_prompt="""
You are an expert in nutrionist where you have to
 "Provide detailed nutrition information for food in a serving size of serving.
  provide the exact deatil with every food item with its name with its calories intake "
 provide me like below format:
 1. Item 1-no. of calories
 2. Item 2-no. of calories...
 --------
 --------

 also mention that the food is healthy or not
                "Include calorie count, macronutrient breakdown (protein, carbs, fats), and a health analysis. "
                "Suggest healthier alternatives if applicable."
"""


if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.header("The Response Is")
    st.write(response)


