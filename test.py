import cv2

# Initialize the camera
cam = cv2.VideoCapture(0)

# Get frame dimensions
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

# # Load the Haar Cascade for face detection
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    # Capture frame-by-frame 1

    ret, frame = cam.read()
    if not ret:
        break

    height, width, _ = frame.shape

    # Display the resulting frame 5
    cv2.imshow('Frame', frame)
    
    # Break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break

# When everything is done, release the capture
cam.release()
cv2.destroyAllWindows()


# Release the capture and writer objects
# cam.release()
# cv2.destroyAllWindows()