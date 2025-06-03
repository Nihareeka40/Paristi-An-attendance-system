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
    "22DCS040":
        {
            "name": "Nihareeka Makwana",
            "Department": "CSE",
            "enrollment_year": 2022,
            "Semester": 4,
            "Last_attendance_time": "2025-02-02 09:15:01"
        },
    "22DCS033":
            {
                "name": "Yashvi Kashundra",
                "Department": "CSE",
                "enrollment_year": 2022,
                "Semester": 4,
                "Last_attendance_time": "2025-02-02 10:15:01"
            }

}

for key, value in data.items():
    ref.child(key).set(value)
