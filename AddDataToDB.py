import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "firebase_url"
})

ref = db.reference('Students')

data = {
    #GUI to enter data using pygame or tkinter
    "21DCS111":
        {
            "name": "Kush Shah",
            "Department": "CSE",
            "enrollment_year": 2021,
            "Semester": 4,
            "Last_attendance_time": "2023-02-02 09:15:01"
        },
    "21DCS200":
            {
                "name": "Narendra Modi",
                "Department": "PMO",
                "enrollment_year": 2021,
                "Semester": 4,
                "Last_attendance_time": "2023-02-02 10:15:01"
            }

}

for key, value in data.items():
    ref.child(key).set(value)
