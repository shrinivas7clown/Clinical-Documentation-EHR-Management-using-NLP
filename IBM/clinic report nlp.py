import spacy
import json
import re

# Load spaCy model (default: en_core_web_sm, replace with 'en_core_sci_sm' for medical NLP)
try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("Downloading spaCy model...")
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Sample Clinical Notes
clinical_notes = [
    """
    Patient: John Doe, Age: 45
    Chief Complaint: Persistent cough and fever for 5 days.
    Diagnosis: Suspected pneumonia. Prescribed Azithromycin 500mg for 5 days.
    Medical History: Hypertension, Type 2 Diabetes.
    """,
    """
    Patient: Jane Smith, Age: 32
    Chief Complaint: Severe headache and nausea.
    Diagnosis: Migraine. Prescribed Sumatriptan 50mg.
    Medical History: No known conditions.
    """
]

# Function to extract entities from clinical text
def extract_medical_info(text):
    doc = nlp(text)
    
    extracted_info = {
        "Patient Name": "",
        "Age": "",
        "Symptoms": [],
        "Diagnosis": "",
        "Medications": [],
        "Medical History": []
    }

    # Extract patient name and age using regex
    name_match = re.search(r"Patient:\s*([\w\s]+),", text)
    age_match = re.search(r"Age:\s*(\d+)", text)
    
    if name_match:
        extracted_info["Patient Name"] = name_match.group(1).strip()
    if age_match:
        extracted_info["Age"] = age_match.group(1)

    # Extract medical entities
    for ent in doc.ents:
        if ent.label_ in ["DISEASE", "CONDITION"]:  # Example categories
            extracted_info["Diagnosis"] = ent.text
        elif ent.label_ == "MEDICATION":
            extracted_info["Medications"].append(ent.text)
        elif ent.label_ == "SYMPTOM":
            extracted_info["Symptoms"].append(ent.text)

    # Extract medical history
    history_match = re.search(r"Medical History:\s*(.*)", text)
    if history_match:
        extracted_info["Medical History"] = [h.strip() for h in history_match.group(1).split(",")]

    return extracted_info

# Process multiple clinical notes
ehr_records = [extract_medical_info(note) for note in clinical_notes]

# Convert to JSON format
ehr_json = json.dumps(ehr_records, indent=4)

# Save to a file
with open("ehr_output.json", "w") as file:
    file.write(ehr_json)

# Output results
print("Extracted EHR Data:")
print(ehr_json)