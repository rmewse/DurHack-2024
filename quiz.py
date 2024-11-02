''' 1. Display Question
2. Display answers
3. Keep record of answers
4. Be able to click confirm'''

#read questions from csv?
# Please access the library’s documentation here: https://docs.python.org/3/library/csv.html
import csv
import streamlit as st
import pandas as pd
st.write("Hello World")



#! need to change
def create_question_list(question_file):
    question_data=[]
    #open file in read mode
    with open(question_file,'r') as file:
        #read file in dictionary format
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            new_question={}
            new_question['question']=row["Question"]
            new_question['options']=row["Option A"], row["Option B"], row["Option C"], row["Option D"]
            question_data.append(new_question)
    return question_data

question_file='DinoQuestions.csv'
create_question_list(question_file)
#!need to rewrite 
def image(question):
    client_id = "4Vwaw-8lwS3_QfivsLzQNvWsRhKyjiTNMXsqJ2OS7ao"
    client_secret = ""
    redirect_uri = ""
    code = ""

    auth = Auth(client_id, client_secret, redirect_uri, code=code)
    api = Api(auth)
    import requests
    import pygame

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
def quiz_app():
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
            question_placeholder.write(f"*question['question'].strip('""')*")
            for option in question['options']:
                options_placeholder.write(option)


quiz_app()
