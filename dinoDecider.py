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
        print("red dino")
        print(affirmation)

    #if they have answered b the most
    elif b>a and b>c and b>d:
        print("orange dino")
        print(affirmation)
    
    #if they have answered c the most
    elif c>a and c>b and c>d:
        print("yellow dino")
        print(affirmation)

    #if they have answered d the most
    elif d>a and d>b and d>c:
        print("green dino")
        print(affirmation)

    #if they have answered a and b equally AND c and d equally
    elif a==b and c==d:
        print("blue dino")
        print(affirmation)
    
    #if they have answered a and b equally AND c and d not equally
    elif a==b and c!=d:
        print("purple dino")
        print(affirmation)

    #if they have answered a and b not equally AND c and d equally
    elif a!=b and c==d:
        print("violet dino")
        print(affirmation)


