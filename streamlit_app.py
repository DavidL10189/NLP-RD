#NLP R&D App - OS I/F

#Modules
import streamlit as st
import os
import google.generativeai as ggi


#Get API Key from Secrets file into a variable
apikey = st.secrets["API_KEY"]

#UI - Title
st.title("Troy and OS Interface chatbox")

#Apply our Gemini API Key
ggi.configure(api_key = apikey)

#Create instance of Google LLM
geminiModel = ggi.GenerativeModel("gemini-1.5-pro")

#Use factory to return chat object
geminiChat = geminiModel.start_chat()

#Prompt the user to input their request
userQuestion = st.text_input("You can ask the model about Troy University or about how to perform Windows OS tasks")
#submitButton = st.button("Send your question to Gemini")

#Functionality to perform the communication with the API
if userQuestion:
    #Send the question to Gemini and get the response
    geminiResponse = geminiChat.send_message(userQuestion,stream=False)
    #Display the response in the page's UI
    st.subheader("Gemini's Response: ")    
    for word in geminiResponse:
        st.text(word.text)
        #