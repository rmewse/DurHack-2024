import random

a = int(input("Input a"))
b = int(input("Input b"))
c = int(input("Input c"))
d = int(input("Input d"))

def dinoDecide(a,b,c,d):
    #reads a random line from the text file
    num = random.randint(0,18)
    with open('Assets/Affirmations.txt','r') as file:
        content = file.readlines()
        affirmation = (content[num]).strip()

    #if they have answered a the most
    if a>b and a>c and a>d:
        print(affirmation)
        return "Assets/blue.PNG"

    #if they have answered b the most
    elif b>a and b>c and b>d:
        print(affirmation)
        return "Assets/green.PNG"
    
    #if they have answered c the most
    elif c>a and c>b and c>d:
        print(affirmation)
        return "Assets/grey.PNG"

    #if they have answered d the most
    elif d>a and d>b and d>c:
        print(affirmation)
        return "Assets/orange.PNG"

    #if they have answered a and b equally AND c and d equally
    elif a==b and c==d:
        print(affirmation)
        return "Assets/purple.PNG"
    
    #if they have answered a and b equally AND c and d not equally
    elif a==b and c!=d:
        print(affirmation)
        return "Assets/red.PNG"

    #if they have answered a and b not equally AND c and d equally
    elif a!=b and c==d:
        print(affirmation)
        return "Assets/yellow.PNG"


