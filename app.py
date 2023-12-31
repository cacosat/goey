# -*- coding: utf-8 -*-

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# Load API key from .env and set variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    st.error("OAI key not found")
    st.stop()

assistant_id="asst_JWkej3uysAiE0ZEiZP7ixziN"
client = OpenAI(api_key=openai_api_key)

model_instructions = "The GPT's primary role is to act as a digital mentor for entrepreneurs, guiding them in the development and monetization of their ideas. It will focus on helping users understand the needs of their target audience, emphasizing empathy and user-centric approaches. All this done through a guiding framework based on design thinking and its different stages: Discovery (contains a bit of the classical stage Empathize and a bit of Define); Ideation; Prototype; Testing; Implementation. The GPT will avoid technical design terminology and instead recommend paths of development using tools from design thinking methodologies (like in-depth interviews, benchmarks, surveys, ideation excercises like brainwritting, prototyping and testing tools, etc.), guiding users in their construction and application. The GPT should provide support and guidance for project development, aiding users in transforming an idea into a product, service, or venture. It should also encourage creativity and practical problem-solving, tailored to the unique needs of each entrepreneur. The GPT will clarify any ambiguities in user requests, aiming to provide the most relevant and useful advice. It will maintain a friendly and encouraging tone, fostering a supportive environment for entrepreneurial growth."


# Streamlit

st.set_page_config(page_title="Goey", page_icon=":speech_balloon:")   

st.title("Goey Chat")
st.write("Welcome to Goey Chat! Goey is your assistant, designed to help you develop ideas and ventures into profitable businesses.")

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Buttons

col1, col2 = st.columns(2)

with col1:
    if st.button("Start Chat"):
        st.session_state.start_chat = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

with col2:
    if st.button("Exit Chat"):
        st.session_state.messages = []  # Clear the chat history
        st.session_state.start_chat = False  # Reset the chat state
        st.session_state.thread_id = None

# Chat session started

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4-1106-preview"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    #Display existing messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Checking for a message from the user and setting it to "prompt" with added placeholder
    if prompt := st.chat_input("Ask Goey!"):
        # appending message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Adding prompr as message (content) of user (role)
        client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
        )

        # Creating a "run" so the model reads the thread and responds to the user
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions=model_instructions
        )
        # Wait for the run to complete
        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
            
        # List of messages added to the thread
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)

else:
    st.write("Click 'Start Chat' to begin.")