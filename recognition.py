import sys
print("Python executable in quiz v2.py:", sys.executable)

try:
    import pygame
    print("Pygame imported successfully.")
except ImportError:
    print("Pygame could not be imported.")

import cv2
import numpy as np
import subprocess # Used to run another python file
import time
import pygame
import threading


last5dir = []

current_dir = ""

def timer():
    return_val = ""
    def run():
        time.sleep(10)
        return_val = current_dir
        
    thread = threading.Thread(target = run)
    thread.start()
    
    sent = False
    
    while sent==False:
        if return_val != "":
            print(return_val)
            return return_val
    
def recog_gesture(prev_center, cur_center):
    
    # Check if there is a previous center
    if prev_center is None:
        return None
    
    # Get movement of hand
    dx = cur_center[0] - prev_center[0]
    dy = cur_center[1] - prev_center[1]
    
    
    # Threshold for the amount of pixels the hand has to move to be recognised
    threshold = 50
    if abs(dy) < abs(dx): # This is a horizontal movement, we need to distinguish between left/right
        if dx > threshold:
            return "Right"
        elif dx < -threshold:
            return "Left"
    else: # This is a vertical movement
        if dy > threshold:
            return "Down"
        elif dy < -threshold:
            return "Up"
        
    # If none of the conditions for direction recognition
    return None
    
    

last5dir = []

def recog_gesture(prev_center, cur_center):
    
    # Check if there is a previous center
    if prev_center is None:
        return None
    
    # Get movement of hand
    dx = cur_center[0] - prev_center[0]
    dy = cur_center[1] - prev_center[1]
    
    
    # Threshold for the amount of pixels the hand has to move to be recognised
    threshold = 50
    if abs(dy) < abs(dx): # This is a horizontal movement, we need to distinguish between left/right
        if dx > threshold:
            return "Right"
        elif dx < -threshold:
            return "Left"
    else: # This is a vertical movement
        if dy > threshold:
            return "Down"
        elif dy < -threshold:
            return "Up"
        
    # If none of the conditions for direction recognition
    return None
    
# Makes sure the form cannot be opend twice
opened = False

# Initialize the camera
cam = cv2.VideoCapture(0)

# Used for hand recog
previous_center = None

# Define the range for hand color detection in HSV
lower_colour = np.array([0, 50, 50])    # Adjust to match your color
upper_colour = np.array([10, 255, 255])

# Get frame dimensions
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

print(str(frame_width) + " " + str(frame_height))


# This is the image to be overlayed onto the camera display
border_img = cv2.resize(cv2.imread("Assets/border.png", cv2.IMREAD_UNCHANGED),(frame_width,frame_height))

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Record the start time for the 10-second timer
start_time = time.time()
counter = 0
while True:
    try:
        ret, frame = cam.read()
        if not ret:
            break
        
        flipped_frame = cv2.flip(frame, 1)

        # Check if 10 seconds have passed
        elapsed_time = time.time() - start_time
        
        if opened == True:
            
            # Used for hand tracking
            hsv = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2HSV)
            
            mask = cv2.inRange(hsv, lower_colour, upper_colour)
         
            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            # Find the biggest hand, only recognise one hand
            if contours:
                # Largest hand
                largest_hand = max(contours, key=cv2.contourArea)
                
                x,y,w,h = cv2.boundingRect(largest_hand)
                
                
                current_center = (x + w // 2, y + h // 2) # Find the center of the hand box
                
                if (previous_center == None):
                    previous_center = current_center
                    
                gesture = recog_gesture(previous_center,current_center)
                
                previous_center = current_center # Update centers to track movement
                
                counter = counter + 1
                print(counter)
                if counter > 80: 
                    break
                if len(last5dir) < 5:
                    last5dir.append(gesture)
                else:
                    last5dir = last5dir[1:]
                    last5dir.append(gesture)
                
                print(last5dir)
                #Getting the count of each direction
                leftCount = last5dir.count("Left")
                rightCount = last5dir.count("Right")
                upCount = last5dir.count("Up")
                downCount = last5dir.count("Down")
                # Store counts in a dictionary
                counts = {
                    "Left": leftCount,
                    "Right": rightCount,
                    "Up": upCount,
                    "Down": downCount
                    }
                maxDirection = max(counts, key=counts.get)
                current_dir = maxDirection
                print(maxDirection)
                with open('myTextFile.txt', 'w') as file:
                    file.write(maxDirection)
                    file.close()
        # Overlay the border image      
        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Only the largest face will be detected and used
        largest_face = None
        max_area = 0
        
        # Find largest face by area
        for (x, y, w, h) in faces:
            size = h * w
            if size > max_area:
                max_area = size
                largest_face = (x, y, w, h)  # This is the face that will be used for processing
                
        # Initialise x, y, w, h for largest face
        if largest_face is not None:
            x, y, w, h = largest_face
            cv2.rectangle(flipped_frame, (x, y), (x + w, y + h), (100, 84, 48), 5)  # Draw blue rectangle

        # Add text above the rectangle when a face is recognized
        cv2.putText(flipped_frame, "Smile! Then, Press Enter To Continue!", (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        # Create a background for the text
        text = "Smile! Then, Press Enter To Continue!"
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]

        # Background rectangle coordinates
        background_x1 = x
        background_y1 = y - text_size[1] - 10  # 10 pixels above the text
        background_x2 = x + text_size[0]
        background_y2 = y
        
        # Create a blue background with some padding
        text_background = np.zeros((text_size[1] + 10, text_size[0] + 10, 3), dtype=np.uint8)
        text_background[:] = (100, 84, 48)  # Blue background (BGR format)

        # Draw the background rectangle
        cv2.rectangle(flipped_frame, (background_x1, background_y1), (background_x2, background_y2), (100, 84, 48), cv2.FILLED)

        text_x = x + (text_size[0] // 2) - (background_x1 + 5)
        text_y = y - 5
        
        # Add the text on top of the background
        cv2.putText(flipped_frame, text, (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        #Overlay the border image (with alpha blending if it has transparency)
        if border_img.shape[2] == 4:  # Check if the overlay has an alpha channel
            # Separate the color and alpha channels
            overlay_rgb = border_img[:, :, :3]
            overlay_alpha = border_img[:, :, 3] / 255.0

            # Blend the overlay with the frame
            for c in range(0, 3):
                flipped_frame[:, :, c] = (overlay_alpha * overlay_rgb[:, :, c] + (1 - overlay_alpha) * flipped_frame[:, :, c])


        # Write the frame with detected faces to the output file
        out.write(flipped_frame)

        # Display the captured frame with detected faces
        cv2.imshow('Camera', flipped_frame)

        # Press 'Enter' key to perform an action
        key = cv2.waitKey(1)
        if key == 13:  # 13 is the ASCII code for Enter
            if (opened == False):
                # Testing confirmation
                print("Enter key pressed! Performing action...") 
                
                # Screenshot the area that is highlighted by blue box
                face_img = flipped_frame[y:y + h, x:x + w]
                cv2.imwrite("face_img_recent.png", face_img)
                
                # Open question form
                subprocess.Popen([sys.executable, "quiz v2.py"])
                opened = True
            
        # Press 'q' to exit the loop
        if key == ord('q'): 
            break
    except:
        pass

# Release the capture and writer objects
cam.release()
out.release()
cv2.destroyAllWindows()
