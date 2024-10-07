from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, image[0], prompt])
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

st.set_page_config(page_title="Car Inspector")

st.header("Car Inspector")
car_brand = st.text_input("Enter car brand: ", key="car_brand")
car_color = st.text_input("Enter car color: ", key="car_color")
car_type = st.text_input("Enter car type: ", key="car_type")
chassis = st.text_input("Enter chassis number: ", key="chassis")
plate_number = st.text_input("Enter plate number: ", key="plate_number")
# part_name = st.text_input("Enter part name: ", key="part_name")
# part_price = st.text_input("Enter part price: ", key="part_price")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Predict Car Repair Price")

input_prompt = """
You have provided the following information:
- Car Brand: {car_brand}
- Car Color: {car_color}
- Car Type: {car_type}
- Chassis Number: {chassis}
- Plate Number: {plate_number}
- Part Name: {part_name}
- Part Price: {part_price}

Please upload an image of the car for better estimation of repair cost. Please tell the cost in saudi riyal. Examine the picture and try to calculate the total cost. Can you specify the damaged area also
"""

## If submit button is clicked

if submit:
    if car_brand and car_color and car_type and chassis and plate_number:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt.format(car_brand=car_brand, car_color=car_color, car_type=car_type, chassis=chassis, plate_number=plate_number, part_name=part_name, part_price=part_price), image_data, "")
        st.subheader("The Response is")
        st.write(response)
    else:
        st.warning("Please provide all the required information.")
