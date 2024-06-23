#Research & Development App - OS Natural Language Interface

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

#Modules
import streamlit as st
import os
import google.generativeai as ggi
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings

#Variables to hold our different documents to be used
fileTroy = "RAGDocuments/prompt_answer.csv"
fileOS = "RAGDocuments/prompt_OS_answer.csv"


#Get API Key from Secrets file into a variable
apikey = st.secrets["API_KEY"]

#Function to load a document
def DocLoader(fileName):
   loader = CSVLoader(fileName, csv_args={'delimiter':','})
   return loader.load()

#Function to split a document
#Chunking sizes chosen should cover entire lines and overlap parts of contiguous lines
def DocSplitter(document):
   splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=200)
   #context = "\n\n".join(str(p.page_content) for p in document)
   #return splitter.split_text(context)
   return splitter.split_documents(document)

#Load our documents used for RAG
loadedTroy = DocLoader(fileTroy)
loadedOS = DocLoader(fileOS)

#Split our documents
troy_Split = DocSplitter(loadedTroy)
OS_Split = DocSplitter(loadedOS)

#Create embeddings object
embeddings = GoogleGenerativeAIEmbeddings(model="models/embeddings-001",google_api_key=apikey)
st.write(len(troy_Split))
#Use Troy csv chunks and embeddings to create vectorDB
vector_index = Chroma.from_documents(troy_Split, embeddings)#.as_retriever(search_kwargs={"k":1})

#Text to display status to the user
headerDisplay = "Hello"
detailDisplay = "Please ask a question above"

st.title("Gemini assistant & :red[NLP OS I/F R&D]")

#Create Gemini AI object. Apply the Gemini API Key. Set temperature to help with strong matches
lcGemini = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=apikey,temperature=0.2,convert_system_message_to_human=True)

#Prompt the user to input their request
userQuestion = st.text_area("You can ask general questions, questions about Troy University, and in the future interface with your OS! Press **CTRL+Enter** to send your question.")

responseTitle = st.empty()
responseTitle.write("")
responseBody = st.empty()
responseBody.write("")


#Functionality to perform the communication with the API
if userQuestion:
   responseTitle.write("Processing")
   responseBody.write("")
   userQuestion_Prompt = PromptTemplate.from_template("{userQuestion}")
   lcChain = LLMChain(llm=lcGemini, prompt = userQuestion_Prompt, verbose=True)
   lcResponse = lcChain.run(userQuestion)
   responseTitle.write("")
   responseBody.write(lcResponse)