import xml.etree.ElementTree as ET
import os
from formatDrugNames import formatDrugName

output = open("medications.txt", "w")

# Dictionary: (medication type, count)
medication_types = {}
# Dictionary: (medication, count)
medications = {}
# List of dictionaries: (medication type, count), indexed by patient
medication_types_per_patient = [{} for i in range(450)]
# List of dictionaries: (medication, count), indexed by patient
medications_per_patient = [{} for i in range(450)]

directory = 'Project2-newdata'
for filename in os.listdir(directory):
    if not "c" in filename and not "i" in filename:
        curr_patient = int(filename[:3])
        # print(curr_patient)

        tree = ET.parse(directory + '/' + filename)
        root = tree.getroot()

        for medication_tag in root.iter('MEDICATION'):
            # Only parse inner medication tags
            if len(medication_tag.attrib) > 4:
                medication_type1 = medication_tag.attrib['type1']
                medication_type2 = medication_tag.attrib['type2']
                medication = medication_tag.attrib['text']
                medication = formatDrugName(medication, output)

                # Add medication_type to medication_types dictionary
                if medication_type1 in medication_types:
                    medication_types[medication_type1] += 1
                else:
                    medication_types[medication_type1] = 1

                if medication_type2 != "":
                    if medication_type2 in medication_types:
                        medication_types[medication_type2] += 1
                    else:
                        medication_types[medication_type2] = 1

                # Add medication_type to patient-level medication_types dictionary
                if medication_type1 in medication_types_per_patient[curr_patient]:
                    medication_types_per_patient[curr_patient][medication_type1] += 1
                else:
                    medication_types_per_patient[curr_patient][medication_type1] = 1

                if medication_type2 != "":
                    if medication_type2 in medication_types_per_patient[curr_patient]:
                        medication_types_per_patient[curr_patient][medication_type2] += 1
                    else:
                        medication_types_per_patient[curr_patient][medication_type2] = 1

                # Add medication to mediction dictionary
                if medication in medications:
                    medications[medication] += 1
                else:
                    medications[medication] = 1

                # Add medication to patient-level medication dictionary
                if medication in medications_per_patient[curr_patient]:
                    medications_per_patient[curr_patient][medication] += 1
                else:
                    medications_per_patient[curr_patient][medication] = 1

output.close()

#print('MEDICATION TYPES:')
# print(medication_types)
#print('MEDICATION TYPES PER PATIENT:')
# print(medication_types_per_patient)
print('MEDICATIONS:')
print(medications)
#print('MEDICATIONS PER PATIENT:')
# print(medications_per_patient)
