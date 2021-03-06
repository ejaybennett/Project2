import xml.etree.ElementTree as ET
import os
from formatDrugNames import formatDrugName
from extractVitals import extractVitalSign
output = open("medications3.txt", "w")

def dictionary_union(a,b):
	c = b
	for k in a.keys():
		c[k] = a[k]
	return c


# Dictionary: (medication type, count)
medication_types = {}
# Dictionary: (medication, count)
medications = {}
# Dictionary: (vital, count)
vitals = {}
# List of dictionaries: (medication type, count), indexed by patient
medication_types_per_patient = [{} for i in range(450)]
# List of dictionaries: (medication, count), indexed by patient
medications_per_patient = [{} for i in range(450)]
# List of dictionaries: (vitalIndicator, value), indexed by patient
vitals_per_patient = [{} for i in range(450)]
directory = 'Project2-newdata'
i = 0
for filename in os.listdir(directory):
    i += 1
    if not "c" in filename and not "i" in filename:
        curr_patient = int(filename[:3])
        print("FILE: ", i, " ", "PATIENT: ", curr_patient)
        # print(curr_patient)

        tree = ET.parse(directory + '/' + filename)
        root = tree.getroot()
        try:
            print("VITALS")
            text = root[0].text
            p = extractVitalSign(text)
            #print(p)
            vitals_per_patient[curr_patient] = p
            for v in p.keys():
                print(v,":",str(p[v]))
                if v in vitals:
                    vitals[v] = vitals[v] + 1
                else:
                    vitals[v] = 1
        except Exception as e:
            print(e)
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

output.write('Medication types:\n')
output.write(str(medication_types) + '\n')
output.write('Medication types per patient:\n')
output.write(str(medication_types_per_patient) + '\n')
output.write('Medications:\n')
output.write(str(medications) + '\n')
output.write('Medications per patient:\n')
output.write(str(medications_per_patient) + '\n')
output.write('Vitals:\n')
output.write(str(vitals) + '\n')
output.write('Medications per patient:\n')
output.write(str(vitals_per_patient) + '\n')
output.close()

master_patient_dictionary = [dictionary_union(dictionary_union(medications_per_patient[i] ,\
                                                               medication_types_per_patient[i]),\
                                              vitals_per_patient[i])\
                             for i in range(len(vitals_per_patient))]
columns = ["Patient Number"] + list(vitals.keys()) + list(medications.keys()) +\
          list(medication_types.keys())
import csv
with open('master_excel.csv', 'w') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames = columns)
	writer.writeheader()
	for data in master_patient_dictionary:
		writer.writerow(data)
#print('MEDICATION TYPES:')
# print(medication_types)
#print('MEDICATION TYPES PER PATIENT:')
# print(medication_types_per_patient)
# print('MEDICATIONS:')
# print(medications)
#print('MEDICATIONS PER PATIENT:')
# print(medications_per_patient)
