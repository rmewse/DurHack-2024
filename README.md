# Affirasaurus
What it does
- Solves the problem of Mental Health
- This does Facial Recognition of the user
- Creates a user friendly quiz where the user can select the options by moving themselves to the right, left, up or down. 
- The results of the quiz are stored and analysed to give the user their most like dino representation. 
- Gives a lovely positive affirmation at the end

How we made it
- Did Facial Recognition using cv2 and a lovely border
- Stored the image of the user in our system when they pressed the enter key
- Detected the movement of the users through a coordinate system
- Using pygame created a user friendly quiz system which 10 questions and 4 options
- Created a tutorial page for new users
- Tracked the users movements using previous functions
- Analysed the results given by the user
- Through this we decided on a unique dino for each user
- Generated a unique quote and positive affirmation for each user

The Art
- The following art has been drawn by us (we love it!!)
    - blue.PNG -> blue dino
    - border.PNG -> border when doing facial recognition
    - green.PNG -> green dino
    - grey.PNG -> grey dino
    - orange.PNG -> orange dino
    - purple.PNG -> purple dino
    - red.PNG -> red dino
    - yellow.PNG -> yellow dino

Furture Development
- The following respresent the features we would've added if we were to continue this project
    -Create a hands free game where the user does not have to press any keys. 
    - Implement eye-tracking
    - Make this into an application
    - Have faster execution of some processes using GPUs
    - Use a neural network when assigning dinos
    - Create a bank of questions where the program would randomly pick 10 questions

How it links to all the themes
- Solves the real world problem of mental health through dinos (what more could you want!)
- Hackiest Hack
- rgb() was inverted
- Don't know why it happened -> there was an instance where we opened the quiz window and it keep self replicating in an infinite loop like a virus and we do not know why this happened and how we fixed it. The main thing is that we did solve it. Hooray!
- Computatioanlly complex - When testing for the user we found that there was a bottleneck because our program was going too fast and the user could not keep up
- Over the top - Look at our program
- Dino Theme
- Dino Quotes
- Over engineered because of gestures. We could've done a click when selecting the answers to the questions but we went above and beyond to impress you guys. 