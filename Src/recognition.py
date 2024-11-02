import cv2
import numpy as np
import streamlit
import subprocess # Used to run another python file

# Initialize the camera
cam = cv2.VideoCapture(0)

# Get frame dimensions
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

print(str(frame_width) + " " + str(frame_height))

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    try:
        ret, frame = cam.read()
        if not ret:
            break
        
        flipped_frame = cv2.flip(frame, 1)

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

        # Write the frame with detected faces to the output file
        out.write(flipped_frame)

        # Display the captured frame with detected faces
        cv2.imshow('Camera', flipped_frame)

        # Press 'Enter' key to perform an action
        key = cv2.waitKey(1)
        if key == 13:  # 13 is the ASCII code for Enter
            print("Enter key pressed! Performing action...") 
            # Here you can add the action you want to perform
            # For example, you might want to move to the next question, save data, etc.
            # You can also break the loop if you want to stop the video capture.
            # break  # Uncomment if you want to stop the loop on Enter

        # Press 'q' to exit the loop
<<<<<<< HEAD
        if cv2.waitKey(1) == ord('q'): 
            break
        elif cv2.waitKey(1) == 32:
            subprocess.run(["python", "../quiz.py"])
    except:
        pass
=======
        elif key == ord('q'):
            break
    except Exception as e:
        print(f"Error: {e}")
>>>>>>> refs/remotes/origin/main

# Release the capture and writer objects
cam.release()
out.release()
cv2.destroyAllWindows()
