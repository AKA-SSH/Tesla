# Importing required libraries
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

# Configuring GenAI with the provided API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Initializing the GenerativeModel from GenAI
tesla = genai.GenerativeModel('gemini-pro-vision')

# Function to get the Tesla model response
def get_tesla_response(configuration_prompt, image, user_prompt):
    """
    Generates content using the Tesla generative model from GenAI.

    Parameters:
    - image (list): A list containing the image data or path.
    - user_prompt (str): The user-provided prompt for generating content.

    Returns:
    str: The generated content in response to the provided image and prompt.
    """
    response = tesla.generate_content([configuration_prompt, image[0], user_prompt], generation_config= {'temperature':0.2})
    return response.text

# Function to convert an uploaded image file into GenAI-compatible format
def image_contents(uploaded_image_file):
    """
    Converts an uploaded image file into a format suitable for GenAI processing.

    Parameters:
    - uploaded_image_file (FileStorage): The uploaded image file.

    Returns:
    list: A list containing a dictionary with image information, including MIME type and data.
    
    Raises:
    FileNotFoundError: If no file is uploaded.
    """
    if uploaded_image_file is not None:
        bytes_data = uploaded_image_file.getvalue()
        image_parts = [{'mime_type': uploaded_image_file.type,
                        'data': bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError('No File Uploaded.')

# configuration prompt
configuration= '''
**Input 2: Element Name**
    - [Your Element]
    - Type of [Your Element]

**Task:**
   
**Calculation and Output:**
    - Calculate and present the V and I values across the specified element in a tabular format for easy comprehension. Include the following table:

      | Element         | Voltage (V)     | Current (I)     |
      |-----------------|-----------------|-----------------|
      | [Your Element]  | [Calculated V]  | [Calculated I]  |

**Calculation Section:**
    - Below the table, provide a section explaining how the V and I values were calculated. Include relevant formulas and steps for clarity.
'''


# Setting up Streamlit app configuration
st.set_page_config(page_title='Tesla')
st.header('Tesla: Circuit Analysis Tool')

# User input and file upload components
user_input = st.text_input(label='Enter the prompt', key='input', value='', placeholder='prompt...')
uploaded_image_file = st.file_uploader(label='Drop Circuit Drawing Here...', type=['jpg', 'jpeg', 'png'])

# Displaying the uploaded image if available
img = ''
if uploaded_image_file is not None:
    img = Image.open(uploaded_image_file)
    st.image(img, caption='Uploaded Circuit Drawing', use_column_width=True)

# Analyze Circuit button
submit = st.button('Analyze Circuit')
if submit:
    # Processing and analyzing the circuit drawing
    with st.spinner(text='Analyzing... Drink some water in the meantime...'):
        image_data = image_contents(uploaded_image_file)
        response = get_tesla_response(configuration, image=image_data, user_prompt=user_input)
        st.write(response)
