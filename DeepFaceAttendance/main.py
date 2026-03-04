import cv2
from deepface import DeepFace
import os
from datetime import datetime

# 1. Configuration
db_path = "dataset"  # Jahan aapki photos hain
attendance_file = "Attendance.csv"

# 2. Attendance Function
def markAttendance(name):
    with open(attendance_file, 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        name_list = [line.split(',')[0] for line in lines]
        if name not in name_list:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
            print(f"Attendance marked for: {name}")

# 3. Camera Start
cap = cv2.VideoCapture(0)
print("DeepFace System Active. Press 'q' to quit.")

while True:
    success, frame = cap.read()
    if not success:
        break

    try:
        # DeepFace detection aur recognition aik saath
        results = DeepFace.find(img_path=frame, 
                                db_path=db_path, 
                                model_name="VGG-Face", 
                                enforce_detection=False, 
                                silent=True)

        if len(results) > 0 and not results[0].empty:
            # Match mil gaya (Pehli entry uthayein)
            match_path = results[0]['identity'][0]
            name = os.path.basename(match_path).split('.')[0].upper()
            
            # Box dimensions
            source_x = int(results[0]['source_x'][0])
            source_y = int(results[0]['source_y'][0])
            source_w = int(results[0]['source_w'][0])
            source_h = int(results[0]['source_h'][0])

            # Drawing
            cv2.rectangle(frame, (source_x, source_y), 
                          (source_x + source_w, source_y + source_h), (0, 255, 0), 2)
            cv2.putText(frame, name, (source_x, source_y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            markAttendance(name)

    except Exception as e:
        # Agar koi face detect na ho toh error na aaye
        pass

    cv2.imshow("DeepFace Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()