import cvzone
import os
import pickle
import numpy as np
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "firebase_url",
    'storageBucket': "storage_url"
})
bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
imgBackground = cv2.imread('Resources/background.png')

# Importing mode images in a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Loading the Encoding File (EncodeGenerator)
print("Loading Encoded file .....")
file = open('EncodeFile.p', 'rb')
encodeListKnownwithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownwithIds
# print(studentIds)
print("Encode file Loaded")


modeType = 0
counter = 0
id = 0
imgStudent = []


while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print("Matches", matches)
        print("FaceDis", faceDis)

        matchIndex = np.argmin(faceDis)
        print("Match Index", matchIndex)

        if matches[matchIndex]:
            # print("ID Detcted :", studentIds[matchIndex])
            # print(faceLoc)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            if bbox:
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                cvzone.cornerRect(imgBackground, bbox, rt=0)
            id = studentIds[matchIndex]
            if counter == 0:
                counter = 1
                modeType = 1
    if counter != 0:
        if counter == 1:
            #data retrieving
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)
            blob = bucket.get_blob(f'Images/{id}.png')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

        cv2.putText(imgBackground, str(studentInfo['Semester']), (861, 125),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(studentInfo['Department']), (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(id), (1006, 493),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        #cv2.putText(imgBackground, str(studentInfo['----']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBackground, str(studentInfo['Semester']), (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBackground, str(studentInfo['enrollment_year']), (1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        offset = (414 - w)//2
        cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

        imgBackground[175:175+260, 909:909+260] = imgStudent


        # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
