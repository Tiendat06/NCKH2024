from app.models.Patient import PatientModel
from flask import jsonify, request

class PatientService:
    def __init__(self):
        self.patient_model = PatientModel()

    def loginPatient(self):
        data = request.get_json()
        # print(data)
        PID = data.get('PID')
        # print(PID)
        patient_data = self.patient_model.loginPatient(PID)

        patient_data['_id'] = str(patient_data['_id'])
        if patient_data:
            return jsonify({
                'status': True,
                'data': patient_data,
                'msg': 'Login successfully !'
            })
        return jsonify({
            'status': False,
            'msg': 'Patient not found !'
        })