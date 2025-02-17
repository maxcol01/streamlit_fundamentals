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
	
	llm = ChatOpenAI(api_key=API_OPENAI)
	retriever = vector_store.as_retriever(search_type="similiraty", 
                                          search_kwargs={"k":k})
	chain = RetrievalQA.from_chain_type(llm=llm, 
                                        chain_type="stuff", 
                                        retriever=retriever)
	answer = chain.invoke(q)
	return answer