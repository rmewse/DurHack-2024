import csv
import pygame
import webbrowser
from unsplash.api import Api
from unsplash.auth import Auth
from PIL import Image
from io import BytesIO
import os
import ast
import time

pygame.init()
global screen_width, screen_height
screen_width, screen_height=1200,700
global screen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)

#colours defined here
#!colour scheme
sage_green=(85, 139, 110)
blue=(204, 255, 255)
dark_green = (10, 33, 15)
green =(53, 255, 105)
cream=(238, 229, 233)
red=(255,0,0)

# create font options
pygame.font.init()
#'PressStart2P-vaV7.ttf'
#!change font
small_text = pygame.font.Font('Atop-R99O3.ttf', 10)
medium_text = pygame.font.Font('Atop-R99O3.ttf', 25)
large_text = pygame.font.Font('Atop-R99O3.ttf', 45)
option_text = pygame.font.Font('Atop-R99O3.ttf', 15)
question_text=pygame.font.Font('Atop-R99O3.ttf',20)
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
question_number=1
global question_list
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
            text = drawText(screen, self.msg, dark_green, rect, self.font_size, aa=False, bkg=None)
            if text: #i.e if there is text left over after printing
                print("Error! The screen was too small for the ", self, "Button")
                
        else:
            text_rect = text_surf.get_rect()
            text_rect.center = ((self.x+(self.width/2)), (self.y+(self.height/2)))
            screen.blit(text_surf, text_rect)
    #!change this to match the gesture    
    def is_selected(self):
        colour_copy=self.colour
        self.colour='red'
        pygame.draw.rect(screen, self.colour, rect)
        self.colour = colour_copy

    def is_clicked(self):
        text_surf= (self.font_size).render(self.msg, True, (0, 0, 0))
        text_width, text_height = text_surf.get_size()
        if self.width<text_width and self.height<text_height:
            self.width = text_width+10
            self.height = text_height+10
        rect = pygame.rect.Rect((self.x,self.y), (self.width, self.height))
        mouse_pos = pygame.mouse.get_pos()
        return rect.collidepoint(mouse_pos)

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

def help_screen():
    help_needed=True
    #needed to get back
    surface_list=[]
    screen_surface = pygame.display.get_surface()
    initial_screen_copy = screen_surface.copy()
    screen_copy=screen_surface.copy()
    surface_list.append(screen_copy)
    screen.fill()
    
    #same mechanism as pause function
    help_surface=pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    pygame.draw.rect(help_surface,(0,0,0,0), [0,0, screen_width, screen_height]) # 4th value is opacity
    screen.blit(help_surface,(0,0))
    pygame.display.flip()
        
    #welcome text
    screen_number=0
    title="The Basics:"
    #!fill this out!!
    text = "Use gestures to make choices, but choose carefully... "
    welcome_title =Button(20,30,screen_width,screen_height*0.1,green ,title ,True, medium_text, 'x')
    welcome_title.draw()
    #welcome message
    welcome_text= Button(50,150,screen_width-150,screen_height-150,green , text,True, medium_text, 'n')
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
    screen.fill(cream)
    
    #same mechanism as pause function
    help_surface=pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    pygame.draw.rect(help_surface,(0,0,0,0), [0,0, screen_width, screen_height]) # 4th value is opacity
    screen.blit(help_surface,(0,0))
    pygame.display.flip()

    #welcome text
    screen_number=0
    #!change this
    titles_list=["Welcome to Affirmosaurus!"]#!
    text_list = [("Use the gestures to make your choices. But choose wisely!")]

    welcome_title =Button(20,30,screen_width,screen_height*0.1,green,titles_list[screen_number] ,True, medium_text, 'x')
    welcome_title.draw()
    #welcome message
    welcome_text= Button(50,150,screen_width-150,screen_height-150,green , text_list[screen_number],True, medium_text, 'n')
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
                if next_button.is_clicked():
                        help_needed=False
                        screen.fill(cream)
                        
                
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
        help_button= Button(300,200,200,100, sage_green, "Help",False, medium_text,'n')
        help_button.draw()
        
        #resume button
        resume_button = Button(0,380,200,100,sage_green, "Resume", False, medium_text, 'x')
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

    if pause == False:
        screen.blit(surface, (0,0))
        pygame.display.flip()

def update_answer():
    pass

def quiz():
    global question_list
    global question_number
    for question in question_list:
        screen.fill(cream)
        current_question=question['question']
        answer_selected=False
        #Pause Button
        pause_button = Button ((screen_width*0.85),(screen_height*0.02),120,100,red, "Menu",True, medium_text,'n')
        pause_button.draw()
        #question
        question_content=str(question_number) + ". " + question['question'].strip('""')            
        #image credits
        image_credit, link = image(question_content)
        credit= Button(720,450, 0,0,green, image_credit,False, small_text, 'n')
        credit.draw()
        #display the question
        question_button=Button((screen_width*0.01), (screen_height*0.07), (screen_width),(screen_height*0.15), green, question_content,True, question_text, 'n')
        question_button.draw()
        # for each option, print a letter and then the text
        for option in question['options']:
            letters=['UP) ','DOWN) ','LEFT) ','RIGHT) '] #ABCD respectively
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
        
        while answer_selected==False:
            pygame.display.update()
            for event in pygame.event.get():
            #quit game
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    if event.key == pygame.K_SPACE:
                        pass
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
            answer=update_answer()
            if answer in ['right','left','up','down']:
                answer_selected=True
                if answer=='up':
                    #confirm
                    a+=1
                elif answer=='down':
                    b+=1
                elif answer=='left':
                    c+=1
                elif answer=='right':
                    d+=1
        if answer_selected==True:
            feedback='Great! Next Question...'
            feedback_display= Button(0,0,500,125,white, feedback,True, medium_text,'c')
            feedback_display.draw()
            pygame.display.flip()
            time.sleep(2)
            answer_selected=False
            question_number+=1


#start screen buttons
new_game_button=Button(0,(screen_height*0.87),0,0, green, "Start!",False, large_text,'x')
help_button= Button((screen_width*0.80),(screen_height*0.1),0,0, green, "Help",False, large_text,'n')

# background image
screen.fill(cream)
background=pygame.image.load("dinosaur.jpg")
background_width,background_height=background.get_size()

#Game title
title_surf= large_text.render("Affirmosaurus", True, (255, 255, 255))
title_width, title_height = title_surf.get_size()
title_rect = title_surf.get_rect()
title_rect.topleft = ((screen_width - title_width)/2, (screen_height-title_height)/2)


#drawing to screen
screen.blit(background, ((screen_width-background_width)/2, (screen_height-background_height)/2))
new_game_button.draw()
help_button.draw()
screen.blit(title_surf, title_rect)
           
                    
pygame.init()                  
running = True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if help_button.is_clicked():
                help_screen()

            elif new_game_button.is_clicked():
                tutorial_screen()
                quiz()
    