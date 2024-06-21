#NLP R&D App - OS I/F

#Modules
import streamlit as st
import os
import google.generativeai as ggi


#Get API Key from Secrets file into a variable
apikey = st.secrets["API_KEY"]

#UI - Title
st.title("Troy and NLP OS IF")

#Apply our Gemini API Key
ggi.configure(api_key = apikey)

#Create instance of Google LLM
geminiModel = ggi.GenerativeModel("gemini-1.5-pro")

#Use factory to return chat object
geminiChat = geminiModel.start_chat()

#Prompt the user to input their request
userQuestion = st.text_input("You can ask the model about Troy Univerity or about how to perform OS tasks")
submitButton = st.button("Send your question to Gemini")

#Functionality to perform the communication with the API
if submitButton and userQuestion: 
    #Send the question to Gemini
    geminiResponse = geminiChat.send_message(userQuestion,stream=True)
    #Display the response in the page's UI
    st.subheader("Gemini's Response: ")    
    for word in geminiResponse:
        st.text(word.text)

