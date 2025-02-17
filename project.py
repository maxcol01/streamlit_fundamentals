import streamlit as st
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import (PyPDFLoader, 
												  Docx2txtLoader, 
												  TextLoader)
import os

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

def chunk_data():
    pass