#Research & Development App - OS Natural Language Interface

#Modules
import streamlit as st
import os
import google.generativeai as ggi
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.document_loaders.csv_loader import CSVLoader

#Variables to hold our different documents to be used
fileTroy = "RAGDocuments/prompt_answer.csv"
fileOS = "RAGDocuments/prompt_OS_answer.csv"

#Function to load a document
def DocLoader(fileName):
   loader = CSVLoader(fileName, csv_args={'delimiter':','})
   return loader.load()

#Load our documents used for RAG
loadedTroy = DocLoader(fileTroy)
loadedOS = DocLoader(fileOS)

st.write(loadedTroy)

#CSVLoader()
#ragDirLoader = DirectoryLoader("RAGDocuments", glob='*.csv"')
#ragDocuments = ragDirLoader.load()

#Get API Key from Secrets file into a variable
apikey = st.secrets["API_KEY"]

st.title("Troy and OS Interface chatbox")

#Apply the Gemini API Key
ggi.configure(api_key = apikey)

#Create instance of Google LLM and create chat object
geminiModel = ggi.GenerativeModel("gemini-1.5-pro")
geminiChat = geminiModel.start_chat()

#Prompt the user to input their request - will use enter in the box
#instead of a button for the user to send the question
userQuestion = st.text_input("You can ask the model about Troy University or about how to perform Windows OS tasks")

#Functionality to perform the communication with the API
if userQuestion:
    #Send the question to Gemini and get the response - use streamed respone
    #for better UI responsiveness.
    geminiResponse = geminiChat.send_message(userQuestion,stream=True)
      
    st.subheader("Gemini's Response: ")    
    
    #Use a temporary string to hold the response    
    responseComplete = ""
    
    #Piece the response together and only write it if it ends in a newline
    for responseChunk in geminiResponse:     
         responseTemp = responseChunk.text
         if "\n" in responseTemp: 
            newlinePos = responseTemp.rfind('\n')
            responseComplete += responseTemp[:newlinePos - 1]
            st.write(responseComplete)
            responseComplete = responseTemp[newlinePos:]                  
         else:
            responseComplete += responseTemp
