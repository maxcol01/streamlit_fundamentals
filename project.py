import streamlit as st
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import (PyPDFLoader, 
												  Docx2txtLoader, 
												  TextLoader)
import os

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
def chunk_data(data, chunk_size=256):
	from langchain.text_splitter import RecursiveCharacterTextSplitter
	text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
	chunks = text_splitter.split_documents(data)
	return chunks