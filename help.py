import csv
import pygame
import webbrowser
from unsplash.api import Api
from unsplash.auth import Auth
from PIL import Image
from io import BytesIO
import os
import ast

pygame.init()
global screen_width, screen_height
screen_width, screen_height=1200,700
global screen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)

#colours defined here
#!colour scheme
green=(0, 155, 0)
blue=(204, 255, 255)
black = (0,0,0)
red =(252,81,48)
white=(255,255,255)
dark_blue= (8,127,140)
# create font options
pygame.font.init()
#'PressStart2P-vaV7.ttf'
#!change font
small_text = pygame.font.Font('PressStart2P-vaV7.ttf', 10)
medium_text = pygame.font.Font('PressStart2P-vaV7.ttf', 25)
large_text = pygame.font.Font('PressStart2P-vaV7.ttf', 45)
option_text = pygame.font.Font('PressStart2P-vaV7.ttf', 15)
question_text=pygame.font.Font('PressStart2P-vaV7.ttf',20)
# 
# the following 'drawText' function can be found at https://www.pygame.org/wiki/TextWrap - date of access: 02/11/2024
# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = 4

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left+7, y+7))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]


    return text
global question_number
question_number=0
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


class Button(object):
    def __init__(self, x, y, width, height, colour, msg,wrap_text, font_size, alignment):
        self.x = x
        self.y = y
        self.colour = colour # must be tuple
        self.msg = msg # must be string
        self.wrap_text = wrap_text
        self.font_size = font_size #font size
        self.alignment = alignment #this will be either y or n in each instance
        self.width=width
        self.height=height

        
    def draw(self):
        pygame.init()
        screen_height = screen.get_height()
        screen_width = screen.get_width()
        # draw on screen
        text_surf= (self.font_size).render(self.msg, True, (0, 0, 0))
        text_width, text_height = text_surf.get_size()
        if self.wrap_text != True and (self.width<=text_width or self.height<=text_height) or (self.width==0) or (self.height==0):
            #dimensions of button are defined by the text it contains
            #or boolean operator used because otherwise program would crash if only one dimension was 0
            text_surf= (self.font_size).render(self.msg, True, (0, 0, 0))
            text_width, text_height = text_surf.get_size()
            self.width = text_width+10
            self.height = text_height+10
        else:
            text_surf= (self.font_size).render(self.msg, True, (0, 0, 0))

        if self.alignment == 'x' or self.alignment =='X':#button centred on x axis
            self.x = (screen_width-self.width)/2
            rect = pygame.rect.Rect((self.x,self.y),(self.width, self.height))
            pygame.draw.rect(screen, self.colour, rect)
            
        elif self.alignment == 'y' or self.alignment =='Y': #button centred on y axis
            self.y = (surface_height-self.height)/2
            rect = pygame.rect.Rect((self.x,self.y),(self.width, self.height))
            pygame.draw.rect(screen, self.colour, rect)

        elif self.alignment == 'c' or self.alignment =='C': #button to be centred on both x and y axis
            self.x = (screen_width-self.width)/2
            self.y = (screen_height-self.height)/2
            rect = pygame.rect.Rect((self.x,self.y),(self.width, self.height))
            pygame.draw.rect(screen, self.colour, rect)
            
        else:#otherwise draw with normal coordinates
            rect = pygame.rect.Rect((self.x,self.y), (self.width, self.height))
            pygame.draw.rect(screen, self.colour, rect)
        if self.wrap_text==True:
            rect = pygame.rect.Rect((self.x,self.y),(self.width, self.height))
            text = drawText(screen, self.msg, black, rect, self.font_size, aa=False, bkg=None)
            if text: #i.e if there is text left over after printing
                print("Error! The screen was too small for the ", self, "Button")
                
        else:
            text_rect = text_surf.get_rect()
            text_rect.center = ((self.x+(self.width/2)), (self.y+(self.height/2)))
            screen.blit(text_surf, text_rect)
    #!change this to match the gesture    
    def is_clicked(self):
        text_surf= (self.font_size).render(self.msg, True, (0, 0, 0))
        text_width, text_height = text_surf.get_size()
        if self.width<text_width and self.height<text_height:
            self.width = text_width+10
            self.height = text_height+10
        rect = pygame.rect.Rect((self.x,self.y), (self.width, self.height))
        mouse_pos = pygame.mouse.get_pos()
        return rect.collidepoint(mouse_pos)

def help_screen():
    help_needed=True
    #needed to get back
    surface_list=[]
    screen_surface = pygame.display.get_surface()
    initial_screen_copy = screen_surface.copy()
    screen_copy=screen_surface.copy()
    surface_list.append(screen_copy)
    screen.fill(blue)
    
    #same mechanism as pause function
    help_surface=pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    pygame.draw.rect(help_surface,(0,0,0,0), [0,0, screen_width, screen_height]) # 4th value is opacity
    screen.blit(help_surface,(0,0))
    pygame.display.flip()
        
    #welcome text
    screen_number=0
    title="The Basics:"
    #!fill this out!!
    text = "Use gestures to make choices"
    welcome_title =Button(20,30,screen_width,screen_height*0.1, blue,title ,True, medium_text, 'x')
    welcome_title.draw()
    #welcome message
    welcome_text= Button(50,150,screen_width-150,screen_height-150, blue, text,True, medium_text, 'n')
    welcome_text.draw()

    #back button
    back_button = Button(40,575, 150, 100, green, "Back", False, medium_text, 'n')
    back_button.draw()
    
    pygame.display.flip()
    
    while help_needed==True:
        pygame.display.update()
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_q:
                    running = False
                    pygame.quit()
            #!gonna have to go through this        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked():
                    help_needed=False
                    screen.blit(initial_screen_copy, (0,0))
                    pygame.display.flip()
                    

def tutorial_screen():
    help_needed=True
    #needed to get back to screen before help was clicked
    surface_list=[]
    screen_surface = pygame.display.get_surface()
    initial_screen_copy = screen_surface.copy()
    screen_copy=screen_surface.copy()
    surface_list.append(screen_copy)
    screen.fill(blue)
    
    #same mechanism as pause function
    help_surface=pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    pygame.draw.rect(help_surface,(0,0,0,0), [0,0, screen_width, screen_height]) # 4th value is opacity
    screen.blit(help_surface,(0,0))
    pygame.display.flip()

    #welcome text
    screen_number=0
    titles_list=["Welcome to EarthSaver:Climate Challenge","1. The Basics:","2. Objectives", "3. Levels:"]
    text_list = [("This is the ultimate climate change simulator game where you, the newly elected leader, have the power to shape the future of our planet for the next 30 years. Your mission is to make decisions that will help combat climate change, maintain a healthy budget, and save the Earth from environmental disasters."), ("Before you embark on your journey as Earth's leader, you'll take a multiple-choice test to gauge your initial knowledge about climate change. After the game, you'll take the test again to see how much you've learned. You start the game with 100 budget points. Every decision you make costs a certain number of points, so spend wisely! If you run out of budget points, you lose the game."),(" Your goal is to keep the global temperature from rising too high. You can monitor this in the stats bar, alongside sea level rise and the current global temperature. Pay attention to the trends and make decisions to stabilize or reduce the temperature. "),("There are three levels in the game, each containing 10 situations. In each situation, you'll be presented with four options. Choose wisely to ensure a sustainable and safe future for the planet. Top tip: Be cautious! If you choose options that harm the environment, surprise tipping points may occur. These unexpected events will deduct points from your budget, making it even more challenging to achieve your goals. Click next if you're ready to begin!")]
    #rename vars!
    welcome_title =Button(20,30,screen_width,screen_height*0.1, blue,titles_list[screen_number] ,True, medium_text, 'x')
    welcome_title.draw()
    #welcome message
    welcome_text= Button(50,150,screen_width-150,screen_height-150, blue, text_list[screen_number],True, medium_text, 'n')
    welcome_text.draw()
    #next button
    next_button = Button(1000,575, 150, 100, green, "Next", False, medium_text, 'n')
    next_button.draw()

    
    pygame.display.flip()
    
    while help_needed==True:
        pygame.display.update()
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_q:
                    running = False
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.is_clicked() and screen_number<3:
                    screen_surface = pygame.display.get_surface()
                    screen_copy = screen_surface.copy()
                    surface_list.append(screen_copy)
                    help_surface.fill(blue)
                    welcome_title =Button(20,30,screen_width,screen_height*0.1, blue,titles_list[screen_number+1] ,True, large_text, 'x')
                    welcome_title.draw()
                    #welcome message
                    welcome_text= Button(50,150,screen_width-150,screen_height-150, blue, text_list[screen_number+1],True, medium_text, 'n')
                    welcome_text.draw()
                
                    pygame.display.flip()
                    if screen_number<3:
                        screen_number+=1
                        next_button.draw()
                elif next_button.is_clicked() and screen_number ==3:
                        help_needed=False
                        screen.fill(blue)
                        
                

pause = False

def pause_screen(pause, surface):
    pause_surface= pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    if pause== True:
        #needed for pause function
        screen_surface = pygame.display.get_surface()
        screen_copy = screen_surface.copy()
        pygame.draw.rect(pause_surface,(128,128,128,150), [0,0, screen_width, screen_height]) # 4th value is opacity
        screen.blit(pause_surface,(0,0))
        pygame.display.flip()
        
        #help button
        help_button= Button(300,200,200,100, green, "Help",False, medium_text,'n')
        help_button.draw()
        
        #save button
        save_button = Button(700,200,200,100,green, "Save", False, medium_text, 'n')
        save_button.draw()

        
        #resume button
        resume_button = Button(0,380,200,100,dark_blue, "Resume", False, medium_text, 'x')
        resume_button.draw()
        
        #update the display
        pygame.display.flip()
        
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if help_button.is_clicked():
                        help_screen()
                        pause=True
                    elif resume_button.is_clicked():
                        pause=False
                    elif save_button.is_clicked():
                        save()
                    

                    

    if pause == False:
        screen.blit(surface, (0,0))
        pygame.display.flip()

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
    
    # Initialize pygame
    pygame.init()

    # Load image from byte data
    image = pygame.image.load(BytesIO(img_data))
    DEFAULT_IMAGE_SIZE = (1000, 375)
 
    # Scale the image to your needed size
    image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)

    # Draw the image to the screen
    screen.blit(image, (50, 65))
    
    
    #link to photographer's profile
    links = user_data["links"]
    profile_link=links["html"]
    
    return name, profile_link


def level_one():
    pause=False
    main_questions=create_main_list(main_list)
    answer=''
    answer_click=False
    screen.fill(blue)
   
    global question_number
    question=main_questions[question_number]

    while question_number<10 and not end:
            question=main_questions[question_number]
            screen.fill(blue)
            if question_number>2:
                undo_button= Button((screen_width*0.5),(screen_height*0.02),120,100,red, "Undo",True, medium_text,'n')
                undo_button.draw()
            answer_click=False
            
            #Pause Button
            pause_button = Button ((screen_width*0.85),(screen_height*0.02),120,100,red, "Menu",True, medium_text,'n')
            pause_button.draw()

            
            #question
            question_content=str(question_number+1) + ". " + question['question'].strip('""')
            #image credits
            image_credit, link = image(question_content)
            credit= Button(720,450, 0,0,blue, image_credit,False, small_text, 'n')
            credit.draw()
            #display the question
            question_button=Button((screen_width*0.01), (screen_height*0.07), (screen_width),(screen_height*0.15), blue, question_content,True, question_text, 'n')
            question_button.draw()
            
            # for each option, print a letter and then the text
            for option in question['options']:
                letters=['a) ','b) ','c) ','d) ']
                #draw option buttons
                if question['options'].index(option)==0: #if this is the first option in the list, since lists in python are zero-indexed
                    option_a=Button((screen_width*0.035),(screen_height*0.65),660, 60,green,letters[question['options'].index(option)]+option.strip('"'),True, option_text,'n')
                    option_a.draw()
                elif question['options'].index(option)==1:
                    option_b=Button((screen_width*0.035),(screen_height*0.74),660,60,green, letters[question['options'].index(option)]+option.strip('"'),True, option_text,'n')
                    option_b.draw()
                elif question['options'].index(option)==2:
                    option_c=Button((screen_width*0.035),(screen_height*0.83),660,60,green, letters[question['options'].index(option)]+option.strip('"'),True, option_text,'n')
                    option_c.draw()
                elif question['options'].index(option)==3:
                    option_d=Button((screen_width*0.035),(screen_height*0.92),660,60,green,letters[question['options'].index(option)]+option.strip('"'),True, option_text,'n')
                    option_d.draw()
            #needed for pause function
            screen_surface = pygame.display.get_surface()
            screen_copy = screen_surface.copy()
            
            #condition controlled loop - so user can only click on a button once to prevent crashing from multiple inputs
            while answer_click==False:
                pygame.display.update()
                #event handler
                for event in pygame.event.get():
                    #quit game
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        #pause
                        if event.key == pygame.K_SPACE:
                            if pause == False:
                                pause=True
                                pause_screen(pause, screen_copy)
                                # inverts the current state of the boolean variable pause so pause can be toggled
                                pause=False
                    #block only runs when game isn't paused
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pause_button.is_clicked():
                            if pause == False:
                                    pause=True
                                    pause_screen(pause, screen_copy)
                                    # inverts the current state of the boolean variable pause so pause can be toggled
                                    pause=False
                        #block only runs when game isn't paused
                    if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                        # Check for mouse click within the text surface area
                        if credit.is_clicked():

                            webbrowser.open(link)
                        #input processing blocks below
                        if question_number>2:
                            if undo_button.is_clicked():
                                undo(undo_screen_copy)
                        if option_a.is_clicked():
                            answer='a'
                            answer_click=True

                        elif option_b.is_clicked():
                            answer='b'
                            answer_click=True

                        elif option_c.is_clicked():
                            answer='c'
                            answer_click=True

                        elif option_d.is_clicked():
                            answer='d'
                            answer_click=True
                        
                        else:
                            pygame.display.update()
                            
 
                        acceptable_answers= ['a','b','c','d']
                        if answer_click==True and answer in acceptable_answers:
                            screen_surface = pygame.display.get_surface()
                            undo_screen_copy = screen_surface.copy()
                            greenhouse_effect, feedback = climate_decisions(main_questions, greenhouse_effect, answer, question_number)
                            temps, temp_rise, temp_changes, time_jumps, total_temp_rise=update_temps(greenhouse_effect, temps, temp_changes, year, albedo, temp_rise)
                            sea_level_rise, sea_levels, albedo = update_sea(temp_changes)
                            #feedback block
                            feedback_display= Button(0,0,500,125,white, feedback,True, medium_text,'c')
                            feedback_display.draw()
                            pygame.display.flip()
                            time.sleep(2)
                                
                            budget = expenses_decisions(main_questions, budget, answer, question_number)
                            budget=endings(budget)
                            year+=1
                            answer_click=True
                                                    
                            #counter is incremented every time a question is answered, so if a user decides to save their game, they will start with the question they haven't answered yet
                            question_number+=1
                        
                            #blit all to screen
                            pygame.display.update()


#start screen
help_button= Button((screen_width*0.80),(screen_height*0.1),0,0, green, "Help",False, large_text,'n')

# background image
screen.fill(blue)
background=pygame.image.load("earth.png")
background_width,background_height=background.get_size()
#Game title
title_surf= large_text.render("Earth Saver", True, (255, 255, 255))
title_width, title_height = title_surf.get_size()
title_rect = title_surf.get_rect()
title_rect.topleft = ((screen_width - title_width)/2, (screen_height-title_height)/2)


#drawing to screen
screen.blit(background, ((screen_width-background_width)/2, (screen_height-background_height)/2))
help_button.draw()