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
def generate_tesla_content(configuration_prompt, image, user_prompt):
    """
    Generates content using the Tesla generative model from GenAI.

    Parameters:
    - image (list): A list containing the image data or path.
    - user_prompt (str): The user-provided prompt for generating content.

    Returns:
    str: The generated content in response to the provided image and prompt.
    """
    response = tesla.generate_content([configuration_prompt, image[0], user_prompt], generation_config={'temperature': 0.2})
    return response.text

# Function to convert an uploaded image file into GenAI-compatible format
def convert_image_to_genai_format(uploaded_image_file):
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
NOTE FOR THE BOT: You are an expert on ciruit analysis, specialising in electronics and network engineering.  Your task is to calculate the current and voltage across the element given by the user.

**Element Identification**
   - Specify the name of the circuit element for which you want to calculate voltage (V) and current (I).

**Task:**

**Calculation and Output:**
   - Calculate and present the voltage (V) and current (I) values across the specified circuit element. Provide the results in a clear tabular format for easy comprehension:

      | Element         | Voltage (V)     | Current (I)     |
      |-----------------|-----------------|-----------------|
      | [Your Element]  | [Calculated V]  | [Calculated I]  |

**Calculation Section:**
   - Below the table, include a section explaining the calculation methodology. Provide relevant formulas and step-by-step instructions for clarity.

Ensure that the circuit diagram is comprehensive, including all necessary components and connections for accurate calculations.
'''

# Streamlit app configuration
st.set_page_config(page_title='Tesla')
st.header('Tesla: Circuit Analysis Tool')

# User input and file upload components
user_input_prompt = st.text_input(label='Enter the prompt', key='input', value='', placeholder='prompt...')
uploaded_image_file = st.file_uploader(label='Drop Circuit Drawing Here...', type=['jpg', 'jpeg', 'png'])

# Displaying the uploaded image if available
uploaded_image = ''
if uploaded_image_file is not None:
    uploaded_image = Image.open(uploaded_image_file)
    st.image(uploaded_image, caption='Uploaded Circuit Drawing', use_column_width=True)

# Analyze Circuit button
submit_button = st.button('Analyze Circuit')
if submit_button:
    # Processing and analyzing the circuit drawing
    with st.spinner(text='Analyzing... Drink some water in the meantime...'):
        # Dynamically replace placeholders in the configuration with user input
        dynamic_configuration = configuration.replace('[Your Element]', user_input_prompt)
        response = generate_tesla_content(dynamic_configuration, image=convert_image_to_genai_format(uploaded_image_file), user_prompt=user_input_prompt)
        st.write(response)