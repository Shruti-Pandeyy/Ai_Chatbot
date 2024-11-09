import streamlit as st
import sqlite3
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import PyPDF2

# Database initialization
def init_db():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY,
            session_id INTEGER,
            role TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Save a message to the database
def save_message(session_id, role, message):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO chats (session_id, role, message) VALUES (?, ?, ?)', (session_id, role, message))
    conn.commit()
    conn.close()

# Export database to .sql file
def export_to_sql():
    conn = sqlite3.connect('chat_history.db')
    with open('chat_history.sql', 'w') as f:
        for line in conn.iterdump():
            f.write(f'{line}\n')
    conn.close()

# Initialize the database
init_db()

def create_llm():
    return HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        max_new_tokens=512,
        temperature=1.5,
        repetition_penalty=1.03,
        task='text-generation',
        return_full_text=True,
    )

llm = create_llm()
prompt_template = """
### [INST]

{context}

### QUESTION:
{question}

[/INST]
"""
prompt = PromptTemplate(
   input_variables=["context", "question"],
   template=prompt_template,
)
llm_chain = LLMChain(llm=llm, prompt=prompt)

st.set_page_config(page_title="PDF Chatbot", page_icon=":robot:")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = 1  # Initialize the first session
    st.session_state.current_chat = []

# Function to start a new conversation
def start_new_conversation():
    st.session_state.session_id += 1  # Increment session ID for new conversation
    st.session_state.current_chat = []  # Clear the current chat history

# Button to start a new conversation
if st.button("Start New Chat"):
    start_new_conversation()

# Display previous sessions
st.write("Previous Conversations:")
for idx in range(1, st.session_state.session_id):  # Loop over past sessions
    if st.button(f"View Conversation {idx}"):
        # Retrieve chat history from the database
        conn = sqlite3.connect('chat_history.db')
        cursor = conn.cursor()
        cursor.execute('SELECT role, message FROM chats WHERE session_id = ?', (idx,))
        chat_history = cursor.fetchall()
        conn.close()
        
        # Display previous chat session
        st.write(f"Conversation {idx}:")
        for role, message in chat_history:
            if role == "user":
                st.write(f"*User:* {message}")
            else:
                st.write(f"*Chatbot:* {message}")
        st.write("---")

# Input for user message and file uploader
user_input = st.text_input("Type your message here...", key="user_input")
uploaded_file = st.file_uploader("Upload a PDF file (optional)", type="pdf", key="pdf_file")

pdf_text = ""
if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text()

if user_input:
    save_message(st.session_state.session_id, "user", user_input)
    st.session_state.current_chat.append({"user": user_input})
    context = pdf_text if pdf_text else "No PDF provided."
    response = llm_chain.invoke({"context": context, "question": user_input})
    text_after_inst = response['text'].split('[/INST]')[-1].strip()
    save_message(st.session_state.session_id, "bot", text_after_inst)
    st.session_state.current_chat.append({"bot": text_after_inst})

# Display current chat history
st.write("Chat History:")
for message in st.session_state.current_chat:
    if "user" in message:
        st.write(f"*User:* {message['user']}")
    elif "bot" in message:
        st.write(f"*Chatbot:* {message['bot']}")

# Export chat history to SQL file
if st.button("Export Chat History"):
    export_to_sql()
    st.write("Chat history exported to chat_history.sql.")

# Hide Streamlit style elements
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
</style>
"""
st.write(hide_streamlit_style, unsafe_allow_html=True)
