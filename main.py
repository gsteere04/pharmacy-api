import json

from fastapi import FastAPI, HTTPException, status

from models import Patient


file_path = "patients.json"
with open(file_path, "r") as json_file:
    data = json.load(json_file)


app = FastAPI()

patients = [Patient(**patient_data) for patient_data in data]

@app.get("/patients")
async def list_patients() -> list[Patient]:
    return patients


@app.post("/patients/{first_name}")
async def new_patient(patient: Patient) -> None:
    global patients
    patients.append(patient)
# Use the first name as the unique identifier. For example, in the PUT route, you'd have something like this: "/patients/{first_name}"

@app.put("/patients/{first_name}")
async def update_patient(first_name: str, updated_patient: Patient) -> Patient:
    global patients

    for i in range(len(patients)):
        if patients[i].first_name == first_name:
            patients[i] = updated_patient
            return updated_patient
        else:
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient does not exist.")


@app.delete("/patients/{first_name}")
async def delete_patient(first_name: str) -> dict:
    global patients

    for i in range(len(patients)):
        if patients[i].first_name == first_name:
            del patients[i] 
            return {"message": "Patient has been removed."}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient does not exist.")
    
