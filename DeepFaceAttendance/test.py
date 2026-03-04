import cv2
from deepface import DeepFace
import os
from datetime import datetime

db_path = "dataset"
attendance_file = "Attendance.csv"


# for marked attendance
def markAttendance(name):
    with open(name, "a+") as f:
        f.seek(0)
        lines = f.readlines()
        name_list = [line.split(',')[0] for line in lines]

        if name not in name_list:
            now = datetime.now()
            date_format = now.strftime('%H,%M,%S')
            f.writelines(f'/n{name},{date_format}')
            print(f'Attendance marked: {name}')


# form camera start
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()


            


markAttendance('Attendance.csv')

