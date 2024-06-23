#Research & Development App - OS Natural Language Interface

#Modules
import streamlit as st
import os
import google.generativeai as ggi
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

#Variables to hold our different documents to be used
fileTroy = "RAGDocuments/prompt_answer.csv"
fileOS = "RAGDocuments/prompt_OS_answer.csv"

#Function to load a document
def DocLoader(fileName):
   loader = CSVLoader(fileName, csv_args={'delimiter':','})
   return loader.load()

#Function to split a document
def DocSplitter(document):
   splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
   return splitter.split_documents(document)

#Text to display status to the user
headerDisplay = "Hello"
detailDisplay = "Please ask a question above"

#Load our documents used for RAG
loadedTroy = DocLoader(fileTroy)
loadedOS = DocLoader(fileOS)

#Split our documents
troy_Split = DocSplitter(loadedTroy)
OS_Split = DocSplitter(loadedOS)

#Get API Key from Secrets file into a variable
apikey = st.secrets["API_KEY"]

st.title("Troy and OS Interface chatbox")

#Apply the Gemini API Key
lcGemini = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=apikey)

#Prompt the user to input their request
userQuestion = st.text_area("You can ask about Troy University or about how to perform Windows OS tasks")

responseTitle = st.empty()

responseTitle.write("Please enter your question above")


#Functionality to perform the communication with the API
if userQuestion:
   responseTitle.write("Processing")
   userQuestion_Prompt = PromptTemplate.from_template("{userQuestion}")
   lcChain = LLMChain(llm=lcGemini, prompt = userQuestion_Prompt, verbose=True)
   lcResponse = lcChain.run(userQuestion)
   responseTitle.write("")
   st.write(lcResponse)