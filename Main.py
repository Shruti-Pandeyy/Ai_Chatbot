import streamlit as st

st.set_page_config(page_title="PDF Chatbot", page_icon=":robot:")  

style = """
<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f0f0f0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.chat-container {
  height: 400px;
  overflow-y: scroll;
  padding: 10px;
  margin-bottom: 20px;
  border-radius: 5px;
  background-color: #f5f5f5;
}

.chat-message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
}

.chat-message.user {
  background-color: #e0e0e0;
  text-align: right;
}

.chat-message.bot {
  background-color: #d0d0d0;
  text-align: left;
}

.input-container {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.input-container input[type="text"] {
  flex-grow: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-right: none;
  border-radius: 5px 0 0 5px;
}

.input-container button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
}

.input-container input[type="file"] {
  margin-left: 10px;
}
</style>
"""

st.write(style, unsafe_allow_html=True) 

st.title("PDF Chatbot")
chat_history = []

user_input = st.text_input("Type your message here...", key="user_input")
uploaded_file = st.file_uploader("Upload a PDF file (optional)", type="pdf", key="pdf_file")

if user_input:
    chat_history.append({"user": user_input})
    response = "**Work in progress:** Replace with your PDF processing logic here"
    chat_history.append({"bot": response})

st.write("Chat History:")
for message in chat_history:
    st.write(f"{message['user']}" if "user" in message else f"**Chatbot:** {message['bot']}")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
</style>
"""
st.write(hide_streamlit_style, unsafe_allow_html=True)
