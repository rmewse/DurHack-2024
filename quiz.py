''' 1. Display Question
2. Display answers
3. Keep record of answers
4. Be able to click confirm'''

#read questions from csv?
# Please access the library’s documentation here: https://docs.python.org/3/library/csv.html
import csv
import streamlit as st
import pandas as pd




question_list = [
    {"question": "What is your favourite continent?",
     "options": ["Africa", "Europe", "Australia", "Antarctica"]},
    {"question": "How long are your arms?",
     "options": ["Weirdly Short", "Average", "Not Quite Average", "Very long"]},
    {"question": "What is your favourite food?",
     "options": ["Steak", "Salad", "Chicken Salad", "Fruits"]},
    {"question": "Choose an animal",
     "options": ["Shark", "Bird", "Cheetah", "Rhinoceros"]},
    {"question": "What best describes you?",
     "options": ["Relaxed", "Intelligent", "Competitive", "Stressed"]},
    {"question": "How do you spend your weekends?",
     "options": ["Clubbing", "Sleeping", "Reading", "Working"]},
    {"question": "What genre of music do you listen to?",
     "options": ["Classical", "Indie", "Rock", "Rap"]},
    {"question": "What is most important to you?",
     "options": ["Love", "Loyalty", "Money", "Health"]},
    {"question": "What type of zodiac sign are you?",
     "options": ["Earth", "Fire", "Water", "Air"]}
]

#!need to rewrite 
def image(question):
    client_id = "4Vwaw-8lwS3_QfivsLzQNvWsRhKyjiTNMXsqJ2OS7ao"
    client_secret = ""
    redirect_uri = ""
    code = ""

    auth = Auth(client_id, client_secret, redirect_uri, code=code)
    api = Api(auth)
    import requests

    category = str(question)
    # Fetch image data
    url = f"https://api.unsplash.com/photos/random?query={category}&orientation=landscape&client_id=4Vwaw-8lwS3_QfivsLzQNvWsRhKyjiTNMXsqJ2OS7ao"
    data = requests.get(url).json()
    img_data = requests.get(data["urls"]["regular"]).content
    
    #credits
    user_data = data["user"]
    name= user_data["name"] + " /unsplash"
    
    '''# Initialize pygame
    pygame.init()

    # Load image from byte data
    image = pygame.image.load(BytesIO(img_data))
    DEFAULT_IMAGE_SIZE = (1000, 375)
 
    # Scale the image to your needed size
    image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)

    # Draw the image to the screen
    screen.blit(image, (50, 65))'''
    
    
    #link to photographer's profile
    links = user_data["links"]
    profile_link=links["html"]
    
    return name, profile_link

#following function adapted from https://medium.com/@fesomade.alli/building-a-quiz-app-in-python-using-streamlit-d7c1aab4d690
# Function to display a question
def quiz_app(question_list):
    # create container
    with st.container():
        i=0
        for question in question_list:
            number_placeholder = st.empty()
            question_placeholder = st.empty()
            options_placeholder = st.empty()
            results_placeholder = st.empty()
            expander_area = st.empty()
            current_question=i+1
            question_content=question['question'].strip('""')
            number_placeholder.write(f"*Question {current_question}*")
            question_placeholder.write(question['question'])
            for option in question['options']:
                if question['options'].index(option)==0:
                    optionA= st.button(option)
                elif question['options'].index(option)==1:
                    optionB= st.button(option)
                elif question['options'].index(option)==2:
                    optionC= st.button(option)
                elif question['options'].index(option)==3:
                    optionD= st.button(option)
            i+=1


quiz_app(question_list)
