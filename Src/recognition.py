import cv2

# Initialize the camera
cam = cv2.VideoCapture(0)

# Get frame dimensions
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

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
        for (x,y,w,h) in faces:
            size = h*w
            if size > max_area:
                max_area = size
                largest_face = (x,y,w,h) # This is the face that will be used for processing
                
        # Initialise x,y,w,h for largest face
        if largest_face != None:
            x,y,w,h = largest_face
            cv2.rectangle(flipped_frame, (x, y), (x + w, y + h), (100,84,48), 5)  # Draw blue rectangle


        # Write the frame with detected faces to the output file
        out.write(flipped_frame)

        # Display the captured frame with detected faces
        cv2.imshow('Camera', flipped_frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break
    except:
        pass

# Release the capture and writer objects
cam.release()
out.release()
cv2.destroyAllWindows()