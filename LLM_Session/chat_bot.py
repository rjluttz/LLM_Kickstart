"""
Conversational Chat with Document
"""

import os
import streamlit as st
from langchain_community.llms.ollama import Ollama
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader


model_id = 'Eomer/gpt-3.5-turbo'
# load LLM
llm = Ollama(model=model_id)


# function to clear history for fresh chat
def clear_history():
    if 'history' in st.session_state:
        del st.session_state['history']

# keep title for page
st.title('Chat with Document')

# define file uploader
uploaded_file = st.file_uploader(
    "Upload your document (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=False
)

# add the uploaded file 
add_file = st.button("Add file", on_click=clear_history)

# after upload process document
if uploaded_file and add_file:
    with st.spinner('Loading the text content...'):
        # read the file
        bytes_data = uploaded_file.read()

        upload_dir = "./uploaded_docs"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # store the read file
        file_name = os.path.join(upload_dir, uploaded_file.name)

        with open(file_name, 'wb') as f:
            f.write(bytes_data)

        # load the document
        name, extension = os.path.splitext(file_name)

        if extension == ".pdf":
            loader = PyPDFLoader(file_name)
        elif extension == ".docx":
            loader = Docx2txtLoader(file_name)
        elif extension == ".txt":
            loader = TextLoader(file_name)
        else:
            st.write("Document format is not supported !")

        documents = loader.load()
        st.success('File loaded successfully')

    with st.spinner('Processing the text content...'):
        # tokenization
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=100
        )
        chunks = text_splitter.split_documents(documents=documents)

        # get vector embeddings
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

        # Check if vector store already exists
        persist_directory = "./vector_store"

        if os.path.exists(persist_directory) and os.listdir(persist_directory):
            print("✅ Loading existing vector store...")
            vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        else:
            print("🚀 Creating new vector store...")
            vector_store = Chroma.from_documents(chunks, embeddings, persist_directory=persist_directory)
            vector_store.persist()

        # define a retriever
        retriever = vector_store.as_retriever()

        # chain the steps
        chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)

        st.session_state['chain'] = chain
        st.success('File processed successfully')


# get the question from user
question = st.text_input('Input your question')

if question:
    if 'chain' in st.session_state:
        chain = st.session_state['chain']

        if 'history' not in st.session_state:
            st.session_state['history'] = []

        response = chain.run(
            {
                'question': question,
                'chat_history': st.session_state['history']
            }
        )

        st.session_state['history'].append((question, response))
        st.write(str(response))
else:
    # get answer even if document not uploaded
    response = llm.invoke(question)

    st.write(str(response))
