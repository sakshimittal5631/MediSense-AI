import pandas as pd
import pickle
import ast

sym_des = pd.read_csv("datasets/symtoms_df.csv")
precautions = pd.read_csv("datasets/precautions_df.csv")
workout = pd.read_csv("datasets/workout_df.csv")
description = pd.read_csv("datasets/description.csv")
medications = pd.read_csv("datasets/medications.csv")
diets = pd.read_csv("datasets/diets.csv")
doctors = pd.read_csv("datasets/doctors.csv")
svc = pickle.load(open("models/svc.pkl", "rb"))


def helper(dis):
    desc = " ".join(description[description['Disease'] == dis]['Description'])
    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]

    med = []
    med_raw = medications[medications['Disease'] == dis]['Medication'].values
    for m in med_raw:
        if isinstance(m, str):
            try:
                parsed = ast.literal_eval(m)
                if isinstance(parsed, list):
                    med.extend(parsed)
                else:
                    med.append(parsed)
            except (ValueError, SyntaxError, TypeError):
                med.append(m)
        else:
            med.append(m)

    die = []
    diet_raw = diets[diets['Disease'] == dis]['Diet'].values
    for d in diet_raw:
        if isinstance(d, str):
            try:
                parsed = ast.literal_eval(d)
                if isinstance(parsed, list):
                    die.extend(parsed)
                else:
                    die.append(parsed)
            except (ValueError, SyntaxError, TypeError):
                die.append(d)
        else:
            die.append(d)

    wrkout = workout[workout['disease'] == dis]['workout']

    doc_data = doctors[doctors['Disease'].str.strip().str.lower() == dis.strip().lower()][
        ['DoctorName', 'Specialization', 'Hospital']
    ].to_dict(orient="records")

    return desc, [col for col in pre.values], med, die, wrkout, doc_data
