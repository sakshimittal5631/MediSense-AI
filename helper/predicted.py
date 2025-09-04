from datasets.data import diseases_list, symptoms_dict
import pickle
import numpy as np

svc = pickle.load(open("models/svc.pkl", "rb"))


def get_predicted_value(patient_symptoms):
    vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([vector])[0]]
