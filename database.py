import sqlite3

DATABASE = "medigrid.db"

def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            doctor_name TEXT,
            medicine_name TEXT,
            dosage TEXT,
            frequency TEXT,
            duration TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_prescription(data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    for medicine in data["medicines"]:
        cursor.execute("""
            INSERT INTO prescriptions (
                patient_name, doctor_name, medicine_name, dosage, frequency, duration
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["patient_name"],
            data["doctor_name"],
            medicine["name"],
            medicine["dosage"],
            medicine["frequency"],
            medicine["duration"]
        ))
    conn.commit()
    conn.close()

def get_prescriptions():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            patient_name,
            doctor_name,
            medicine_name,
            dosage,
            frequency,
            duration
        FROM prescriptions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    prescriptions = []

    for row in rows:

        prescriptions.append({
            "id": row[0],
            "patient_name": row[1],
            "doctor_name": row[2],
            "medicine_name": row[3],
            "dosage": row[4],
            "frequency": row[5],
            "duration": row[6]
        })

    return prescriptions
if __name__ == "__main__":
    create_database()
    print("Database created successfully!")