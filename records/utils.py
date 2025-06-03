def generate_patient_record_json(record):
    return {
        "patient": {
            "id": record.patient.id,
            "full_name": record.full_name,
            "age": record.age,
            "gender": record.gender,
        },
        "doctor": {
            "id": record.doctor.id if record.doctor else None,
            "name": str(record.doctor.get_full_name()) if record.doctor else "Unknown"
        },
        "visit": {
            "visit_date": record.visit_date.isoformat(),
            "follow_up_date": record.follow_up_date.isoformat() if record.follow_up_date else None,
            "diagnosis": record.diagnosis,
            "treatment_plan": record.treatment_plan,
            "notes": record.notes,
            "vitals": {
                "blood_pressure": record.blood_pressure,
                "temperature": str(record.temperature),
                "pulse_rate": record.pulse_rate
            }
        },
        "prescriptions": [
            {
                "drug_name": p.drug_name,
                "dosage": p.dosage,
                "frequency": p.frequency,
                "duration": p.duration
            } for p in record.prescriptions.all()
        ]
    }
