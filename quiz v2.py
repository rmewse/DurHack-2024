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
    def is_selected(self):
        colour_copy=self.colour
        self.colour='red'
        pygame.draw.rect(screen, self.colour, rect)
        self.colour = colour_copy


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
    #!change this
    titles_list=["Welcome to EarthSaver:Climate Challenge","1. The Basics:","2. Objectives", "3. Levels:"]
    text_list = [("This is the ultimate climate change simulator game where you, the newly elected leader, have the power to shape the future of our planet for the next 30 years. Your mission is to make decisions that will help combat climate change, maintain a healthy budget, and save the Earth from environmental disasters."), ("Before you embark on your journey as Earth's leader, you'll take a multiple-choice test to gauge your initial knowledge about climate change. After the game, you'll take the test again to see how much you've learned. You start the game with 100 budget points. Every decision you make costs a certain number of points, so spend wisely! If you run out of budget points, you lose the game."),(" Your goal is to keep the global temperature from rising too high. You can monitor this in the stats bar, alongside sea level rise and the current global temperature. Pay attention to the trends and make decisions to stabilize or reduce the temperature. "),("There are three levels in the game, each containing 10 situations. In each situation, you'll be presented with four options. Choose wisely to ensure a sustainable and safe future for the planet. Top tip: Be cautious! If you choose options that harm the environment, surprise tipping points may occur. These unexpected events will deduct points from your budget, making it even more challenging to achieve your goals. Click next if you're ready to begin!")]
    #rename vars
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

    if pause == False:
        screen.blit(surface, (0,0))
        pygame.display.flip()


