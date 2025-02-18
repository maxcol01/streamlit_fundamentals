import streamlit as st
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import (PyPDFLoader, 
												  Docx2txtLoader, 
												  TextLoader)
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

# Loading API key
API_OPENAI = os.getenv("API_OPENAI")


# Loading the document into a Langchain format
def load_document(file):
    _, extension = os.path.splitext(file)
    print(f"Loading {file}")
    if extension == ".pdf":
        loader = PyPDFLoader(file)
    elif extension == ".docx":
        loader = Docx2txtLoader(file)
    elif extension == ".txt":
        loader = TextLoader(file)
    else:
        print("Document format is not supported")
        return None

    print("Ok...")
    data = loader.load()
    return data


# Chunking the loaded document
def chunk_data(data, chunk_size=256, chunk_overlap=20):
	from langchain.text_splitter import RecursiveCharacterTextSplitter
	text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
	chunks = text_splitter.split_documents(data)
	return chunks


# Create embeddings and vector store
def create_embeddings(chunks):
	embeddings = OpenAIEmbeddings(api_key=API_OPENAI)
	vector_store = Chroma.from_documents(chunks, embeddings)
	return vector_store


# Create a Q/A function
def ask_and_get_answer(vector_store, q, k=3):
	from langchain.chains import RetrievalQA
	from langchain.chat_models import ChatOpenAI
	
	llm = ChatOpenAI(api_key=API_OPENAI, model="gpt-4o-min")
	retriever = vector_store.as_retriever(search_type="similiraty", 
                                          search_kwargs={"k":k})
	chain = RetrievalQA.from_chain_type(llm=llm, 
                                        chain_type="stuff", 
                                        retriever=retriever)
	answer = chain.invoke(q)
	return answer

import streamlit as st
import os

if __name__ == "__main__":
    # Get the API key 
    #st.image()
    st.subheader("LLM Question-Answering Application")
    
    with st.sidebar:
        document_type = ["pdf", "docx", "txt"]
        uploaded_file = st.file_uploader("Upload a file:", type=document_type)
        chunk_size = st.number_input("Chunk size", min_value=100, max_value=2028, value=512)
        k = st.number_input("k", min_value=1, max_value=20, value=3)
        add_data = st.button("Add Data")
        if uploaded_file and add_data:

            with st.spinner("Reading, chunking and embedding file ... "):
                # Save the uploaded file
                bytes_data = uploaded_file.read()
                file_name = os.path.join("./", uploaded_file.name)
            
            with open(file_name, mode="wb") as f:
                f.write(bytes_data)
            
            # Assuming load_document, chunk_data, and create_embeddings functions are defined
            data = load_document(file_name)
            chunks = chunk_data(data, chunk_size=chunk_size)
            
            # Display chunk information
            st.write(f"Chunk size: {chunk_size}, Chunks: {len(chunks)}")
            
            # Create embeddings and store in session state
            vector_store = create_embeddings(chunks)
            
            st.session_state.vs = vector_store  # Corrected session_state usage
            
            st.success("File uploaded, chunked and embedded successfully")

    q = st.text_input("Ask a question about the content of your file:")
    if q:
        if "vs" in st.session_state:
            vector_store = st.session_state.vs
            st.write(f"k:{k}")# a higher k value will take longer but will be more accurate
            answer = ask_and_get_answer(vector_store, q, k)
            st.text_area("LLM answer: ", value=answer)