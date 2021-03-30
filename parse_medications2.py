import xml.etree.ElementTree as ET
import os
from formatDrugNames import formatDrugName

output = open("medications4.txt", "w")

medication_list = []  # ["medication1", "medication2", ...]
medication_type_list = []  # ["medication_type1", "medication_type2", ...]
# {"patient1": ["medication1", medication2], "patient2": [...], ...}
medication_patient = {}
# {"note1": ["medication1", medication2], "note2": [...], ...}
medication_note = {}
# {"patient1": ["medication_type1", medication_type2], "patient2": [...], ...}
medication_type_patient = {}
# {"note1": ["medication_type1", medication_type2], "note2": [...], ...}
medication_type_note = {}
directory = 'Project2-newdata'
i = 0
for filename in os.listdir(directory):
    i += 1
    if not "c" in filename and not "i" in filename:
        curr_patient = filename[:3]
        if not (curr_patient in medication_patient):
            medication_patient[curr_patient] = []
            medication_type_patient[curr_patient] = []
        curr_note = filename[:6]
        if not (curr_note in medication_note):
            medication_note[curr_note] = []
            medication_type_note[curr_note] = []

        print("ITERATION: ", i, " ", "FILENAME ", curr_note)

        tree = ET.parse(directory + '/' + filename)
        root = tree.getroot()

        for medication_tag in root.iter('MEDICATION'):
            # Only parse inner medication tags
            if len(medication_tag.attrib) > 4:
                medication_type1 = medication_tag.attrib['type1']
                medication_type2 = medication_tag.attrib['type2']
                medication = medication_tag.attrib['text']
                medication = formatDrugName(medication, output)

                # Add medication_type to medication_type_list
                if not (medication_type1 in medication_type_list):
                    medication_type_list.append(medication_type1)

                if medication_type2 != "":
                    if not (medication_type2 in medication_type_list):
                        medication_type_list.append(medication_type2)

                # Add medication to medication_list
                if not (medication in medication_list):
                    medication_list.append(medication)

                # Add medication_type to patient-level medication_types dictionary
                if not (medication_type1 in medication_type_patient[curr_patient]):
                    medication_type_patient[curr_patient].append(
                        medication_type1)

                if medication_type2 != "":
                    if not (medication_type2 in medication_type_patient[curr_patient]):
                        medication_type_patient[curr_patient].append(
                            medication_type2)

                # Add medication to patient-level medication dictionary
                if not (medication in medication_patient[curr_patient]):
                    medication_patient[curr_patient].append(medication)

                # Add medication_type to note-level medication_types dictionary
                if not (medication_type1 in medication_type_note[curr_note]):
                    medication_type_note[curr_note].append(medication_type1)

                if medication_type2 != "":
                    if not (medication_type2 in medication_type_note[curr_note]):
                        medication_type_note[curr_note].append(
                            medication_type2)

                # Add medication to note-level medication dictionary
                if not (medication in medication_note[curr_note]):
                    medication_note[curr_note].append(medication)

output.write('Medication list:\n')
output.write(str(medication_list) + '\n')
output.write('Medication type list:\n')
output.write(str(medication_type_list) + '\n')
output.write('Medications per patient:\n')
output.write(str(medication_patient) + '\n')
output.write('Medications per note:\n')
output.write(str(medication_note) + '\n')
output.write('Medication types per patient:\n')
output.write(str(medication_type_patient) + '\n')
output.write('Medication types per note:\n')
output.write(str(medication_type_note) + '\n')
output.close()

#print('MEDICATION TYPES:')
# print(medication_types)
#print('MEDICATION TYPES PER PATIENT:')
# print(medication_types_per_patient)
# print('MEDICATIONS:')
# print(medications)
#print('MEDICATIONS PER PATIENT:')
# print(medications_per_patient)
