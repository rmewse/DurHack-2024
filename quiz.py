''' 1. Display Question
2. Display answers
3. Keep record of answers
4. Be able to click confirm'''

#read questions from csv?
# Please access the library’s documentation here: https://docs.python.org/3/library/csv.html
import csv
import streamlit as st
import pandas as pd
import time
global selection_made
selection_made=False
if 'clicked' not in st.session_state:
    st.session_state.clicked = False
def click_button():
    st.session_state.clicked = True
    #st.write('Button clicked!')
    global selection_made
    selection_made=True






#following function adapted from https://medium.com/@fesomade.alli/building-a-quiz-app-in-python-using-streamlit-d7c1aab4d690
# Function to display a question
def quiz_app(question_list):
    # create container
    a=0
    b=0
    c=0
    d=0
    with st.container:
        i=1
        next=False
        for question in question_list:
            next=False
            number_placeholder = st.empty()
            question_placeholder = st.empty()
            options_placeholder = st.empty()
            #results_placeholder = st.empty()
            #expander_area = st.empty()
            current_question=i
            question_content=question['question'].strip('""')
            number_placeholder.write(f"*Question {current_question}*")
            question_placeholder.write(question['question'])
            selection_made=False
            for option in question['options']:
                if question['options'].index(option)==0:
                    optionA= st.button(option)
                elif question['options'].index(option)==1:
                    optionB= st.button(option)
                elif question['options'].index(option)==2:
                    optionC= st.button(option)
                elif question['options'].index(option)==3:
                    optionD= st.button(option)

            while next==False:
                time.sleep(1)
                if optionA:
                    a+=1
                    next=True
                elif optionB:
                    b+=1
                    next=True
                elif optionC:
                    c+=1
                    next=True
                elif optionD:
                    d+=1
                    next=True
            i+=1
            




quiz_app(question_list)
