import streamlit as st
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import PyPDF2

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
chat = ChatHuggingFace(llm=llm)
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
pdf_text = ""
if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text()
if user_input:
    chat_history.append({"user": user_input})
    context = pdf_text if pdf_text else "No PDF provided."
    response = llm_chain.invoke({"context": context, "question": user_input})
    text_after_inst = response['text'].split('[/INST]')[-1].strip()
    chat_history.append({"bot": text_after_inst})

st.write("Chat History:")
for message in chat_history:
    st.write(f"{message['user']}" if "user" in message else f"**Chatbot:** {message['bot']}")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
</style>
"""
st.write(hide_streamlit_style, unsafe_allow_html=True)
