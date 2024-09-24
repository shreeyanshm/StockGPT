import pandas as pd
import streamlit as st
import openai
from streamlit_chat import message

# OpenAI API key setup (use environment variables or other secure methods in production)
openai.api_key = "your-api-key"

# Streamlit page title
st.title("StockGPT With Streamlit and OpenAI")

# Load dataset
df = pd.read_csv("Twitter Stock Market Dataset.csv")
df = df.iloc[:-5]  # Assuming you're excluding the last 5 rows
str1 = df.to_string(index=False)  # Convert DataFrame to a string for display

# Initialize session state for user inputs and responses
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = []

if 'openai_response' not in st.session_state:
    st.session_state['openai_response'] = []

# Function to call OpenAI API using the new chat model
def api_calling(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can also use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are an AI assistant helping with stock market analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=512  # Adjust as needed
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Function to get user text input
def get_text():
    return st.text_input("Write your query here:", key="input")

user_input = get_text()

# Process input and generate a response
if user_input:
    prompt = f"{user_input}\n\n{str1}\n\nThe available data is given above."
    output = api_calling(prompt)
    
    # Store user input and API response in session state
    st.session_state.user_input.append(user_input)
    st.session_state.openai_response.append(output)

# Display the conversation history
if st.session_state['user_input']:
    for i in range(len(st.session_state['user_input'])):
        # Display user input
        message(st.session_state['user_input'][i], key=str(i) + '_user', is_user=True, avatar_style="icons")
        # Display OpenAI response
        message(st.session_state['openai_response'][i], key=str(i) + '_bot', avatar_style="miniavs")

