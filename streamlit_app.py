#NLP R&D App - OS I/F

#Modules
import streamlit as st
import os
import google.generativeai as ggi
from langchain_community.document_loaders.csv_loader import CSVLoader

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
    #Send the question to Gemini and get the response
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