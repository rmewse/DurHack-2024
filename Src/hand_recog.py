import cv2
import numpy as np

# Function to recognise movement of boxes
def recog_gesture(prev_center, cur_center):
   
    # Check if there is a previous center
    if prev_center is None:
        return None
    
    # Get movement of hand
    dx = cur_center[0] - prev_center[0]
    dy = cur_center[1] - prev_center[1]
    
    print(str(dx) + " " + str(dy))
    
    print(str(dx) + " " + str(dy))
    
    # Threshold for the amount of pixels the hand has to move to be recognised
    threshold = 50
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
    return none
    
