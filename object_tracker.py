import cv2
import os
import urllib.request


XML_FILE = "haarcascade_frontalface_default.xml"


if not os.path.exists(XML_FILE):
    print("Downloading required tracking file from OpenCV repository...")
    url = f"https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/{XML_FILE}"
    try:
        urllib.request.urlretrieve(url, XML_FILE)
        print("Download successful!")
    except Exception as e:
        print(f"Error downloading model file: {e}")
        exit()

face_cascade = cv2.CascadeClassifier(XML_FILE)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Tracking Active! Press 'q' on your keyboard to exit.")

object_id = 0
tracked_objects = {}

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    detections = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    current_tracks = {}
    
    
    for (x, y, w, h) in detections:
        cx, cy = x + w//2, y + h//2
        matched_id = None
        
       
        for oid, (ox, oy) in tracked_objects.items():
            distance = ((cx - ox)**2 + (cy - oy)**2)**0.5
            if distance < 50:
                matched_id = oid
                break
                
        if matched_id is None:
            object_id += 1
            matched_id = object_id
            
        current_tracks[matched_id] = (cx, cy)

       
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        label = f"ID {matched_id}: Target"
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    
    tracked_objects = current_tracks

    
    cv2.imshow("CodeAlpha Task 4 - Real-Time Object Detection & Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()