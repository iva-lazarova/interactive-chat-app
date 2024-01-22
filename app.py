import streamlit as st
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.schema import(
     SystemMessage,
     HumanMessage,
     AIMessage
)
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Page layout
st.set_page_config(page_title='Your Personal Assistant', page_icon='🤖')

st.subheader('Your Custom ChatGPT 🤖')

chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)

# Creating the messages (chat history) in the Streamlit session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Creating the sidebar
with st.sidebar:
    # streamlit text input widget for the system message (role)
    system_message = st.text_input(label='System role')
    # streamlit text input widget for the user message
    user_prompt = st.text_input(label='Send a message')

    if system_message:
        if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
            st.session_state.messages.append(
                SystemMessage(content=system_message)
                )

    # st.write(st.session_state.messages)

    # If the user entered a question
    if user_prompt:
        st.session_state.messages.append(
            HumanMessage(content=user_prompt)
        )

        with st.spinner('Working on your request ...'):
            # creating the ChatGPT response
            response = chat(st.session_state.messages)

        # adding the response content to the session state
        st.session_state.messages.append(AIMessage(content=response.content))

# st.session_state.messages
# message(" hi there", is_user=False)
# message("this is the user", is_user=True)

if len(st.session_state.messages) >= 1:
    # If no system message given by user, use default
    if not isinstance(st.session_state.messages[0], SystemMessage):
        (st.session_state.messages.insert(0,
                         SystemMessage(content="You are a helpful assistant")))

for i, msg in enumerate(st.session_state.messages[1:]):
    if i % 2 == 0:
        message(msg.content, is_user=True, key=f"{i} + 🤓") # AI response
    else:
        message(msg.content, is_user=False, key=f"{i} + 🤖") # User's question

