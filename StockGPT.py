import pandas as pd
import streamlit as st
import openai
from streamlit_chat import message

openai.api_key = "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"

st.title("StockGPT With Streamlit and OpenAI")


df = pd.read_csv("Twitter Stock Market Dataset.csv")
df = df.iloc[:-5]
str1 = df.to_string(index=False)


# Initialize session state
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = []

if 'openai_response' not in st.session_state:
    st.session_state['openai_response'] = []

def api_calling(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        #max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message

def get_text():
    input_text = st.text_input("write here", key="input")
    return input_text

user_input = get_text()

x = user_input + "\n" + str1 + "\n" + "the data available is given above"
if user_input:
    output = api_calling(x)
    output = output.lstrip("\n")

    # Store the output
    st.session_state.openai_response.append(user_input)
    st.session_state.user_input.append(output)

message_history = st.empty()

if st.session_state['user_input']:
    for i in range(len(st.session_state['user_input']) - 1, -1, -1):
        # This function displays user input
        message(st.session_state["user_input"][i], 
                key=str(i), avatar_style="icons")
        # This function displays OpenAI response
        message(st.session_state['openai_response'][i], 
                avatar_style="miniavs", is_user=True,
                key=str(i) + 'data_by_user')
